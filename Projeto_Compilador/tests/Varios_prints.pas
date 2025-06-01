program test;
var
   x : real;
   i : integer;
   j : integer;
begin
    x := 12.0;
    i := 10;
    j := 300;
    write('this is some text');
    writeln('unformatted integer ',i);
    writeln('unformatted integer computation ', i*i:4);
    writeln('formatted integer',i:4);
    writeln('formatted integer',j:4);
    writeln('unformatted real ',x);
    write('formatted real');
    write(x:8:2);
    writeln('all in one line');
end.