program ExemploReadln;
var
  nome: string;
  idade: integer;
  altura: real;

begin
  write('Digite seu nome: ');
  writeln;
  readln(nome);
  write('Digite sua idade: ');
  readln(idade);
  write('Digite sua altura (em metros): ');
  readln(altura);
  writeln('=== Dados informados ===');
  writeln('Nome: ', nome);
  writeln('Idade: ', idade, ' anos');
  writeln('Altura: ', altura:0:2, ' metros');
  writeln;
  writeln('Pressione Enter para sair...');
end.