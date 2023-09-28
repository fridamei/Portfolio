-- Fridamei

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity self_test_module is
	generic (
		constant clk_freq : integer := 1e8 -- 100 MHz (10 will model 1 second as 100 ns which gives better visualization during testing in ModelSim)
		);
		
	port (
		signal mclk : in std_logic; -- Connected to 100 MHz oscillator on board
		signal reset : in std_logic;
		signal duty_cycle : out std_logic_vector(7 downto 0)
	);
end entity;

architecture rtl of self_test_module is
	-- ROM-constants
	constant dataWidth: natural := duty_cycle'length;
	constant addrWidth: natural := 5;
	
	-- ROM-signals
	signal ROM_address : std_logic_vector(addrWidth-1 downto 0) := (others => '0'); 
	signal ROM_data : std_logic_vector(dataWidth-1 downto 0); 
	
	-- Clock signals
	signal three_sec_tick : integer := 0;
	signal cnt : integer := 0;
	
	-- ROM declaration
	component ROM is
		generic(
			dataWidth: natural := 8;
			addrWidth: natural := 5);
			-- filename: string := "ROM_data.txt");
		port(
			address: in std_logic_vector(addrWidth-1 downto 0);
			data: out std_logic_vector(dataWidth-1 downto 0)
			);	
		end component;
	
	-- Concurrent statements 
begin 
	
	UNIT_ROM: entity work.ROM(rtl)
		port map(
			address => ROM_address,
			data => ROM_data
		);
		
	SET_OUTPUT: process(mclk, reset)
	begin
		if reset then
			duty_cycle <= (others => '0');
			
		elsif rising_edge(mclk) then
			if three_sec_tick = 0 then -- When updating on 0, the address can be initialized to 0 because it wont increment until three_sec_tick has reached 2
				duty_cycle <= ROM_data;
			end if;
		end if;
	end process;
	
	-- Process to increment three_sec_tick every second (the clock frequency is the number of clock oscillations per second, 
	-- so when counter is equal to the frequency one second has passed).
	THREE_SECONDS_TIMER: process(mclk, reset)
	begin
		if reset then 
			cnt <= 0;
			three_sec_tick <= 0;
			ROM_address <= (others => '0');
		
		elsif rising_edge(mclk) then
		
			-- If the last address is reached, this will inhibit the program to loop through the ROM again
			-- The ROM-address remains stuck on the last address in the ROM, who's value should be 0
			if (unsigned(ROM_address) + 1) = 0 then
				ROM_address <= ROM_address;
				
			else
				if cnt = clk_freq - 1 then
					cnt <= 0;
					if three_sec_tick = 2 then -- three_sec_tick has value 0, 1 and 2 for one whole second each
						three_sec_tick <= 0;
						ROM_address <= std_logic_vector(unsigned(ROM_address) + 1); -- Update which ROM-element to fetch
					else 
						three_sec_tick <= three_sec_tick + 1;
					end if;
				else
					cnt <= cnt + 1;
				end if;
			end if;
		end if; 
	end process;
end rtl;