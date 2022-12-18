function validateForm() {
    let x = document.forms["form"]["email"].value;
    let pass = document.forms["form"]["pwd"].value;
    let pass2 = document.forms["form"]["repwd"].value;
    let name = x
    var userData=[]

    $.ajax({ 
      url: "/api/" + name + "/" 
    }).done(function(res) { 
      userData.push(res.name);
   }); 
    console.log("length",x.length);
    if(x.length!=0){
      console.log("length",userData.length);
      console.log(userData[0])
      
       for(let i=0;i<userData.length;i++)
       {
          if(x==userData[i])
          {
            document.getElementById('log').innerText="User Already Registered .";
            document.getElementById('log').style.display="block";
            return false;
          }
       }
    }
    if (x == "") {
      //alert("Name must be filled out");
      document.getElementById('log').innerText="User Name Can Not Be Null.";
      console.log(document.getElementById('log'));
      document.getElementById('log').style.display="block";
      return false;
    }

    if(pass2=="" || pass=="")
     {
        //alert("Password Fields Can Not be A Null");
        document.getElementById('log').innerText="Password Field can Not be A vacent.";
        document.getElementById('log').style.display="block";
        return false
     }

     if(pass2!=pass)
     {
        document.getElementById('log').innerText="Password Does Not Match";
        document.getElementById('log').style.display="block";
        return false
     }
  }