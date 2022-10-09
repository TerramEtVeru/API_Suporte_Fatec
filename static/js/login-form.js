document.getElementById("button-popup").addEventListener("click", function(){
    document.querySelector(".popup-login").style.display = "flex";
})

document.querySelector(".close-login").addEventListener("click", function(){
    document.querySelector(".popup-login").style.display = "none";
})


function validate(){

    var username=document.getElementById("login-usuario").value;
    var password=document.getElementById("login-senha").value;
    if(username=="admin"&& password=="password")
    {
        return location.replace("https://www.w3schools.com");
    }
    else
    {
        alert("login falho, insira os dados novamente")
    }
}


