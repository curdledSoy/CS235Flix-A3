function change_nav(){
  if(document.getElementById("nav").style.display === 'flex'){
      document.getElementById('content-2').style.marginLeft = '0px'
      document.getElementById("nav").style.display = 'none';
    }
    else {
      document.getElementById('content-2').style.marginLeft = '200px'
      document.getElementById("nav").style.display = 'flex';
    }
}



$(".chosen-select").chosen({width: "100%"});




