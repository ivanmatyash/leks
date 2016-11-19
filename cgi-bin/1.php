<?php 
if(isset($_FILES["myfile"])) // Если файл существует 
{ 
  $catalog = "../image/"; // Наш каталог 
  if (is_dir($catalog)) // Если такой каталог есть 
  { 
    $myfile = $_FILES["myfile"]["tmp_name"]; // Времменый файл 
    $myfile_name = $_FILES["myfile"]["name"]; // Имя файла 
    if(!copy($myfile, $catalog)) echo 'Ошибка при копировании файла '.$myfile_name // Если неудалось скопировать файл 
  } 
  else mkdir('../image/'); // Если такого каталога нет, то мы его создадим 
} 
?>
