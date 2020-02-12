var outputArea = $("#chat-output");

$.ajax({
  url : '/gethistory',
  type : 'POST',
  contentType: "application/json",
  
  success: function(data){

    console.log(data.user)
    
    for (var i=0; i<data.user.length; i++)
    {
       x = data.user[i]
       y = data.bot[i]
       outputArea.append(`
      <div class='bot-message'>
        <div class='message'>
        ${x}
        </div>
      </div>
    `);

    
    outputArea.append(`
      <div class='user-message'>
        <div class='message'>
          ${y}
        </div>
      </div>
    `);
  }

 }});



$( "#button" ).click(function() {
  $('#comment').val('');
  var result;
  var data = {'text' : $("#user-input").val() }
  $.ajax({
  url : '/botresponse',
  type : 'POST',
  data: JSON.stringify(data),
  contentType: 'application/json ;charset=UTF-8',
  
  success: function(data){
    user_result = data.user;
    bot_result = data.bot;

    
    outputArea.append(`
      <div class='bot-message'>
        <div class='message'>
        ${user_result}
        </div>
      </div>
    `);

    setTimeout(function () {
    outputArea.append(`
      <div class='user-message'>
        <div class='message'>
          ${bot_result}
        </div>
      </div>
    `);
  }, 250);

  },
  error: function(textStatus, errorThrown){
    
    console.log(errorThrown);

  }
 });




});







