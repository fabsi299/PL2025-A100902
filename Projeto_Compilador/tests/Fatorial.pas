program Fatorial;
var
	n, i, x, fat: integer;
begin
	write ('Introduza um número inteiro positivo:');
	readln(n);
	fat := 1;
	for i := 1 to n do
		begin
		    {teste teste, 123}
			fat := fat * i;
			x := i+(*1+2*)0;
		end;
	writeln('Fatorial de ', n, ': ', fat);
end.

