import os
import random
from typing import Optional
import argparse
import copy
import numpy as np

from networks import (
    generate_demographic_contact_network,
    household_country_data,
)
from sim_loops_pooled_test import SimulationRunner
from viral_model import ViralExtSEIRNetworkModel, VL_PARAMS


def run_simulation(
    seed: int,
    pop_size: int,
    init_prev: float,
    horizon: int,
    num_groups: int,
    pool_size: int,
    LoD: int,
    beta: float,
    sigma: float,
    lamda: float,
    gamma: float,
    edge_weight: float,
    alpha: float,
    peak_VL: float, 
    pooling_strategy: str,
    distancing_scale: float = None,
    dilute: str = "average",
    country: str = "US",
    output_path: Optional[str] = None,
    save_results: Optional[bool] = True,
    **kwargs,
):
    """Run simulation.

    Args:
        seed: The random seed for the simulation.
        pop_size: The population size.
        init_prev: The initial prevalence.
        horizon: The time horizon of the simulation.
        num_groups: Number of screening groups to split the population into.
        pool_size: Size of the pooled tests in one-stage group testing.
        LoD: The limit of detection of the PCR test.
        beta, sigma, lamda, gamma: The parameters of the SEIRS+ model.
        edge_weight: Weight to assign to intra-household edges.
        alpha: Susceptibility multiplier.
        peak_VL: Peak viral load.
        pooling_strategy: The pooling strategy to use. Must be one of "naive", 
            "correlated", and "correlated_weak".
        distancing_scale: Parameter in generating the population network, which
            prescribes the extent of social distancing. If None, then no social
            distancing is applied.
        dilute: dilution scheme, one of {"average", "sum", "max", "max_average"}
        country: Country whose household size distribution we use.
        output_path: The directory to save the simulation results to.
        save_results: Whether to save the simulation results, default True.

    Returns:
        An instance of `SimulationRunner`.
    """
    # set manual seed
    random.seed(seed)
    np.random.seed(seed)

    # generate social network graph
    demographic_graphs, _, households = generate_demographic_contact_network(
        N=pop_size,
        demographic_data=household_country_data(country),
        distancing_scales=[distancing_scale] if distancing_scale is not None else [],
        isolation_groups=[],
    )

    if distancing_scale is None:
        print("No social distancing applied.")
        G = demographic_graphs["baseline"]
    else:
        G = demographic_graphs[f'distancingScale{distancing_scale}']
    G_weighted = copy.deepcopy(G) # for assigning screening groups / pools only
    for e in G.edges():
        if "weight" not in G[e[0]][e[1]]:
            G[e[0]][e[1]]["weight"] = edge_weight
    for e in G_weighted.edges():
        if "weight" not in G_weighted[e[0]][e[1]]:
            G_weighted[e[0]][e[1]]["weight"] = 10**10

    households_dict = {}
    for household in households:
        for node_id in household["indices"]:
            households_dict[node_id] = household["indices"]

    VL_params = copy.deepcopy(VL_PARAMS)
    VL_params["symptomatic"]["peak_height"] = (peak_VL, peak_VL)
    VL_params["asymptomatic"]["peak_height"] = (peak_VL, peak_VL)

    # initiate SEIR+ model, separate initial infected among E and I_pre
    init_E = int(init_prev * pop_size)//2
    init_Ipre = int(init_prev * pop_size)//2

    model = ViralExtSEIRNetworkModel(
        G=G,
        G_weighted=G_weighted,
        households_dict=households_dict,
        VL_params=VL_params,
        beta=beta,
        beta_Q=0,
        sigma=sigma,
        lamda=lamda,
        gamma=gamma,
        alpha=alpha,
        initE=init_E,
        initI_pre=init_Ipre,
        seed=seed,
        transition_mode="time_in_state"
    )

    # initiate simulation runner
    sim = SimulationRunner(
        model=model,
        pooling_strategy=pooling_strategy,
        T=horizon,
        num_groups=num_groups,
        pool_size=pool_size,
        LoD=LoD,
        seed=seed,
        output_path=output_path,
        save_results=save_results,
        max_dt=0.01,
        dilute=dilute
    )

    # run simulation
    sim.run_simulation()
    return sim


def parse():
    # experiment-running params -- read from command line input
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type = int)
    parser.add_argument("--init_prev", type = float, default = 0.01)
    parser.add_argument("--num_groups", type = int, default = 10)
    parser.add_argument("--pool_size", type = int, default = 10)
    parser.add_argument("--LoD", type = int, default = 174)
    parser.add_argument("--pop_size", type = int, default = 10000)
    parser.add_argument("--horizon", type = int, default = 100)
    parser.add_argument("--beta", type = float, default = 0.2)
    parser.add_argument("--sigma", type = float, default = 0.2)
    parser.add_argument("--lamda", type = float, default = 0.5)
    parser.add_argument("--gamma", type = float, default = 0.25)
    parser.add_argument("--edge_weight", type = int, default = 1000)
    parser.add_argument("--alpha", type = float, default = 1.0)
    parser.add_argument("--country", type = str, default = "US")
    parser.add_argument("--peak_VL", type = float, default = 6) 
    parser.add_argument("--distancing_scale", type = float)
    parser.add_argument("--pooling_method", type = str, nargs = "+", default = ["naive", "correlated"])
    parser.add_argument("--dilute", type = str, default = "average")

    args = parser.parse_args()

    return args


def run_simulation_wrapper(kwargs):
    for pooling_strategy in kwargs["pooling_method"]:
        print(kwargs)
        print("Running simulation with pooling strategy: ", pooling_strategy)
        kwargs_ = copy.deepcopy(kwargs)
        kwargs_["output_path"] = os.path.join(kwargs["output_path"], pooling_strategy)
        _ = run_simulation(
            pooling_strategy=pooling_strategy,
            **kwargs_,
        )
        print("Done running simulation with pooling strategy: ", pooling_strategy, "\n")


if __name__ == "__main__":

    args = vars(parse()) # convert namespace to dict

    path = "../data/raw/" + args["country"]
    for param in [
        "pop_size", "init_prev", "num_groups", "pool_size", "horizon", 
        "beta", "sigma", "lamda", "gamma", "LoD", "edge_weight", "alpha", 
        "peak_VL", "distancing_scale", "dilute"
    ]:
        if args[param] is not None:
            path += f"_{param}={args[param]}"
    path += "/"
    args["output_path"] = path

    run_simulation_wrapper(args)