-- Fridamei

/*

Synchronizes two one-bit inputs parallelly, 
using one double flipflop for each of the input bits.

*/

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity synchronizer is 
	port (
		mclk : in std_logic;
		reset : in std_logic;
		async_a : in std_logic;
		async_b : in std_logic;
		
		synced_a : out std_logic;
		synced_b : out std_logic
	);
end entity;

architecture rtl of synchronizer is
	-- First double flip flop
	signal ff1a : std_logic;
	signal ff2a : std_logic;
	
	-- Second double flip flop 
	signal ff1b : std_logic;
	signal ff2b : std_logic;
begin
	process(mclk, reset)
	begin
		if reset = '1' then
			ff1a <= '0';
			ff1b <= '0';
			ff2a <= '0';
			ff2b <= '0';
		elsif rising_edge(mclk) then
			-- First flip flop
			ff1a <= async_a;
			ff2a <= ff1a;
			
			-- Second flip flop
			ff1b <= async_b;
			ff2b <= ff1b;
		end if;
	end process;
	synced_a <= ff2a;
	synced_b <= ff2b;
end rtl; 
			