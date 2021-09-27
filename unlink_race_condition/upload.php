<?php
    show_source(__FILE__);
    if(isset($_FILES["file"])){
        move_uploaded_file($_FILES["file"]["tmp_name"],"upload/" . $_FILES["file"]["name"]);
        $content = file_get_contents("upload/".$_FILES["file"]["name"]);
        if(strpos($content,"php")){
            echo "this is a php file!!!!!";
        }
        unlink("upload/".$_FILES["file"]["name"]);
}
?>
<!-- this file-uploading isn't that easy ...... -->