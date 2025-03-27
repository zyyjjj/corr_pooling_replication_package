#!/bin/sh

for seed in $(seq 1 10)
do
    python run_meta_simulation_g2.py \
        --seed $seed --init_prev 0.01 --pool_size 10 --LoD 1240 --edge_weight 10 \
        --num_groups 5 --alpha 2 --peak_VL 6 --distancing_scale 50.0 \
        --dilute average --beta 0.1 --pooling_method naive correlated &
done