vcom -work work -2008 -explicit pwm.vhd
vcom -work work -2008 -explicit tb_pwm_module.vhd

vsim -gui work.tb_pulse_width_modulator

run -all
