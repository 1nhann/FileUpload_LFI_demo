<?php
show_source(__FILE__);
if(isset($_GET["file"])){
    $file = $_GET["file"];
    if(preg_match("/flag/",$file)){
        die("no flag !!!");
    }
    include $file;
}