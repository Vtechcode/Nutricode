

// <!-- --------js toggle menu-------- -->


var navLinks = document.getElementById("navLinks")

var menuIcon = document.getElementById("menuIcon")


function showMenu(){
    navLinks.style.right = "0";
    
    menuIcon.style.display = "none"
}

function hideMenu(){
    navLinks.style.right = "-200px";

    
    menuIcon.style.display = "block"
}


// ----open details page-----

var diseaseCol = document.getElementsByClassName("disease-col")


function onItemClick(disease){
    console.log('hello');
    document.getElementById("put").value = disease;
    let form = document.getElementById("form1");
            form.submit();
}
