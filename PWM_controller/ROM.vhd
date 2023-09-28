-- Fridamei

library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.numeric_std.all;
use STD.textio.all;

entity ROM is
	generic(
		dataWidth : natural  := 8;
		addrWidth : natural := 5; -- Need at least 20 numbers, 2^5 = 32 addresses
		filename : string := "ROM_data.txt"
	);
	port(
	address : in std_logic_vector(addrWidth-1 downto 0);
	data : out std_logic_vector(dataWidth-1 downto 0)
	);
end entity;

architecture rtl of ROM is
	type memoryArray is array((2**addrWidth)-1 downto 0) of std_logic_vector(dataWidth-1 downto 0); 

	impure function initializeROM(file_name: string) return memoryArray is
		file init_file : text open read_mode is file_name;
		variable currentLine: line;
		variable result: memoryArray;
	begin
		for i in 0 to (2**addrWidth)-1 loop
			if not endfile(init_file) then
				readline(init_file, currentLine);
				read(currentLine, result(i));
			else
				-- If the file contains less lines than there are addresses, 
				-- the values of the remaining addresses are set to 0
				result(i) := std_logic_vector(to_unsigned(0, dataWidth)); 
			end if;
		end loop;
		return result;
	end function;
	
	constant ROM_DATA: memoryArray := initializeROM(filename); 
	
begin 
	data <= ROM_DATA(to_integer(unsigned(address))); 
	
end rtl;
