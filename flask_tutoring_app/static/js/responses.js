let page = 0;
const size = 3;

get_responses = (review_id, response_count, user_id, csrf_token) => {
    page += 1;
    $.ajax({
      type: 'GET',
      url: `/reviews/${review_id}/responses?page=${page}`,
      success: function(data){
                 for(let i=0; i<data.length; i++){
                    $(`#${review_id}_responses`).append(
                        `<div class=${review_id}_response style=\"margin-left: 5%;\" id=${data[i].uuid}_response>
                        <h5 style=\"font-size: 12px; margin-bottom: 1%\">${data[i].author}</p>
                        <p style=\"font-size: 14px; margin: 1%\">${data[i].body}</p>
                        <p style=\"font-size: 10px; margin: 1%\">${data[i].creation_date}</p></div>`
                    );
                    if (data[i].user_id == user_id){
                        $(`#${data[i].uuid}_response`).append(
                            `<button class=link_like onclick=\"delete_response(\'${data[i].uuid}\', \'${csrf_token}\')\">Usuń</button>`)
                    }
               }
      }});
    $(`#${review_id}_remain_responses`).text(response_count - page*size);
    $(`#btn_${review_id}_hide_responses`).css("display", "inline");
    if (page*size >= response_count){
        $(`#btn_${review_id}_responses`).css("display", "none");
    }
}

hide_responses = (review_id, response_count) => {
    $(`#${review_id}_remain_responses`).text(response_count);
    counter = 0;
    page = 0;
    $(`#btn_${review_id}_responses`).css("display", "inline");
    $(`#btn_${review_id}_hide_responses`).css("display", "none");
    $(`.${review_id}_response`).children().remove();
    $(`.${review_id}_response`).remove();
}

show_add_response = (review_id) => {
    let form = $(`#add_response_form`);
    if (form.css("display") == "block" && form.parent().attr("id") == `review_${review_id}` ){
        form.css("display", "none");
    }
    else{
        form.css("display", "block");
        form.detach().appendTo(`#review_${review_id}`);
        $(`#input_response_review_id`).val(review_id);
    }
}

delete_response = (response_id, csrf_token) => {
    $.ajax({
      type: 'POST',
      url: `/responses/${response_id}/delete`,
      data: {csrf_token: csrf_token},
      success: function(data){
        window.location.reload(true);
      }
});
}
