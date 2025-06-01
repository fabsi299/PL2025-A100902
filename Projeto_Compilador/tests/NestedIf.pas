program NestedIf;

var
    x, y, z: integer;

BEGIN
    x := 2;
    y := 3;
    z := 5;

   if x > y then
    begin
        if x > z then
            writeln(x)
        else
            writeln(z);
    end
    else
    begin
        if y > z then
            writeln(y)
        else
            writeln(z);
    end
END.
