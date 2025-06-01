program BooleanTest;
var
  x: integer;
  a, b: boolean;
begin
  a := true;
  b := false;
  if (a AND (NOT b)) OR (b AND (NOT a)) then
    x := 42
  else
    x := 0;
  writeln(x);
end.
