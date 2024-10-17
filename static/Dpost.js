
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


window.onload = function(){

    let serpaseUser=$(".sr").val()
    let postid=$(".Pid").val()
    $.ajax({
        method:"POST",
        url:"/getcomments/",
        data:{
            "sr":serpaseUser,
            "postid":postid,
        },
        headers:{
            "X-CSRFToken": getCookie('csrftoken'),
        },
    }).done(function(response){
        // console.log(response)
        data=JSON.parse(response)
        loadComments(data)

    })

    function loadComments(data){
        data.forEach(function(data){
            let comment_id = data.pk
            let full_data = data.fields

            $("#mainComments").prepend(
                `
                
                <li class="comment">
                        <a class="pull-left" href="#">
                            <img class="avatar" src="/media/" alt="avatar">
                        </a>
                        <div class="comment-body">
                            <div class="comment-heading">
                                <h4 class="user">${full_data.user_name_Of_liked_user}</h4>
                                <h5 class="time">7 minutes ago</h5>
                            </div>
                            <p>${full_data.comment_txt}</p>
                        </div>
                    </li>

                `
            )

        })

    }
}

$(document).off("submit", ".commentForm").on("submit", ".commentForm", function(){
    let serpaseUser = $(".sr").val();
    let postid = $(".Pid").val();
    let comment_txtV = $("#commentTxt").val();
    console.log(comment_txtV);
    $("#commentTxt").val("");
    $.ajax({
        method: "POST",
        url: "/addcomments/",
        data: {
            "sr": serpaseUser,
            "postid": postid,
            "comment_txt": comment_txtV,
        },
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
        },
    }).done(function(){
        $("#mainComments").prepend(
            `
            
            <li class="comment">
                    <a class="pull-left" href="#">
                        <img class="avatar" src="/media/" alt="avatar">
                    </a>
                    <div class="comment-body">
                        <div class="comment-heading">
                            <h4 class="user">${serpaseUser}</h4>
                            <h5 class="time">7 minutes ago</h5>
                        </div>
                        <p>${comment_txtV}</p>
                    </div>
                </li>

            `
        )
    })
});

$(document).off("click", ".share").on("click", ".share", function(){
    let postslugx;
    postslugx = $(".Pslx").val();
    let linkToCopy=`http://127.0.0.1:8000/detailedpost/${postslugx}`

    navigator.clipboard.writeText(linkToCopy)
})