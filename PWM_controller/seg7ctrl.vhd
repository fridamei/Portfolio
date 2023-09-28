library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity seg7ctrl is 
	port ( 
		mclk : in std_logic; --100MHz default på zedboardet, positive flank 
		reset : in std_logic; --Asynchronous reset, active high 
		velocity : in signed(7 downto 0); -- The velocity from the velocity reader module
		
		abcdefg : out std_logic_vector(6 downto 0); -- Control of segments on display
		c : out std_logic -- Control signal to determine which screen is active, where c = 0 is display0 and c = 1 display1
	);
end entity seg7ctrl;

architecture rtl of seg7ctrl is
	signal abs_vel : std_logic_vector(7 downto 0) := (others => '0');

	signal d0 : std_logic_vector(3 downto 0) := (others => '0'); -- The number to be shown on dislay0
	signal d1 : std_logic_vector(3 downto 0) := (others => '0'); -- The number to be shown on dislay1

	-- refresh rate of display:  (2**clk_cnt_bits/clk_hz) (a periode of one off and one on state of each display)
	constant clk_cnt_bits : integer := 19; -- Must be 4 < n < 20 to not be detected by the human eye, calculations in report. With n = 5, each display is on for 16 clock cycles .
	signal clk_cnt : unsigned(clk_cnt_bits-1 downto 0) := (others => '0'); -- clock counter to controll the on/off period of the displays
	signal active_input : std_logic_vector(3 downto 0) := "0000"; -- Holds the input to be decoded to abcdefg-values (d0 when not c and d1 when c)

begin
	abs_vel <= std_logic_vector(abs(velocity));
	d0 <= abs_vel(3 downto 0);
	d1 <= abs_vel(7 downto 4);
	
	c <= clk_cnt(clk_cnt'high); -- Saves the MSB of the clock counter
	
	--active_input<= d1 when clk_cnt(clk_cnt'high) = '1' else d0; -- Sets active_input according to c (cant read directly from c as this is an output)
	active_input<= d1 when c else d0; -- Sets active_input according to c (cant read directly from c as this is an output)
	
	ENCODE_PROC: process(active_input)
	begin
	with active_input select abcdefg <=
					"1111110" when "0000", -- 0
					"0110000" when "0001", -- 1
					"1101101" when "0010", -- 2
					"1111001" when "0011", -- 3
					"0110011" when "0100", -- 4
					"1011011" when "0101", -- 5
					"1011111" when "0110", -- 6
					"1110000" when "0111", -- 7
					"1111111" when "1000", -- 8
					"1110011" when "1001", -- 9
					"1110111" when "1010", -- 10 (A)
					"0011111" when "1011", -- 11 (B)
					"1001110" when "1100", -- 12 (C)
					"0111101" when "1101", -- 13 (D)
					"1001111" when "1110", -- 14 (E)
					"1000111" when "1111", -- 15 (F)
					"0000000" when others;
		end process;

	-- Process to increment the clock counter every rising edge of the clock
	COUNTER : process(mclk)
		begin
			if rising_edge(mclk) then
				if reset = '1' then
					clk_cnt <= (others => '0');
				else	
					clk_cnt <= clk_cnt + 1;
				end if;
			end if;
		end process;

end rtl;