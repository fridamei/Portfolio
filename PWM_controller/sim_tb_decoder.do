vcom -work work -2008 -explicit quadrature_decoder.vhd
vcom -work work -2008 -explicit tb_quadrature_decoder.vhd

vsim -gui work.tb_quadrature_decoder

add wave -position insertpoint  \
sim:/tb_quadrature_decoder/reset \
sim:/tb_quadrature_decoder/mclk \
sim:/tb_quadrature_decoder/sa \
sim:/tb_quadrature_decoder/sb \
sim:/tb_quadrature_decoder/pos_inc \
sim:/tb_quadrature_decoder/pos_dec

run -all