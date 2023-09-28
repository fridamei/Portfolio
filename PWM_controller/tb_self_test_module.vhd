-- Fridamei

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_self_test_module is
end entity;

architecture bhv of tb_self_test_module is
	
	signal tb_clk : std_logic := '0';
	signal tb_rst : std_logic := '0';
	signal duty_cycle : std_logic_vector(7 downto 0);
	
	constant half_periode : time := 5 ns;

	constant clk_freq : integer := 1e8; -- Modellerer hvert sekund til 100 ns

begin
	UUT_STM: entity work.self_test_module(rtl)
		generic map(
			clk_freq => clk_freq
		)
		
		port map(
			mclk => tb_clk,
			reset => tb_rst,
			duty_cycle => duty_cycle
		);
	
	-- Generate clock signal (the self unit test should set all other inputs)
	tb_clk <= not tb_clk after half_periode;
end bhv;