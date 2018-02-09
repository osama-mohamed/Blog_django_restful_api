$('.comment_reply_button').click(function (event){
    event.preventDefault();
    $(this).parent().next('.comment_reply').fadeToggle();
});