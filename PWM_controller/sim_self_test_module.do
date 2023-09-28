vcom -work work -2008 -explicit ROM.vhd
vcom -work work -2008 -explicit self_test_module.vhd
vcom -work work -2008 -explicit tb_self_test_module.vhd

vsim -gui work.tb_self_test_module

add wave -position insertpoint  \
sim:/tb_self_test_module/duty_cycle \
sim:/tb_self_test_module/tb_clk
add wave -position insertpoint  \
sim:/tb_self_test_module/UUT1/three_sec_tick
add wave -position insertpoint  \
sim:/tb_self_test_module/UUT1/ROM_address
add wave -position insertpoint  \
sim:/tb_self_test_module/UUT1/ROM_data

run 10000 ns
