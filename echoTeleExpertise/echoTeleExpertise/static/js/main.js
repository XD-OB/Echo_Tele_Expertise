function viewPassword()
{
  var passwordInput = document.getElementById('password-field');
  var passStatus = document.getElementById('pass-status');
 
  if (passwordInput.type == 'password'){
    passwordInput.type='text';
    passStatus.className='fa fa-eye-slash';
    
  }
  else{
    passwordInput.type='password';
    passStatus.className='fa fa-eye';
  }
}

function display_send()
{
       document.getElementById('send-result').style.display = 'block';
       document.getElementById('main-buttons').style.display = 'none';
}

function display_req_infos()
{
       document.getElementById('additional_infos').style.display = 'block';
       document.getElementById('main-buttons').style.display = 'none';
}

function display_complete_request()
{
       document.getElementById('complete-request').style.display = 'block';
       document.getElementById('show-incomplete-result').style.display = 'none';
}


function submit_new_profile_img() {
  document.getElementById("form-edit-profile_img").submit();
};

setTimeout(function() {
  $('#message').fadeOut('slow')
}, 3000);