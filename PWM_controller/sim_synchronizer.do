vcom -work work -2008 -explicit ROM.vhd
vcom -work work -2008 -explicit self_test_module.vhd
vcom -work work -2008 -explicit pwm.vhd
vcom -work work -2008 -explicit synchronizer.vhd
vcom -work work -2008 -explicit tb_synchronizer.vhd

vsim -gui work.tb_synchronizer

add wave -position insertpoint  \
sim:/tb_synchronizer/mclk \
sim:/tb_synchronizer/dir \
sim:/tb_synchronizer/en \
sim:/tb_synchronizer/synced_dir \
sim:/tb_synchronizer/synced_en \
sim:/tb_synchronizer/duty_cycle \
sim:/tb_synchronizer/DUT_PWM/mclk_cnt \
sim:/tb_synchronizer/DUT_PWM/pwm_cnt \
sim:/tb_synchronizer/DUT_SELF_TEST/three_sec_tick

run 33 us
