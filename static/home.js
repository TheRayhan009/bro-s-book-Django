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


function dataLoad(){
    let serpes_User = $(".sr").val()
    if (window.innerHeight + window.scrollY > document.body.offsetHeight) {
       $.ajax({
        method:"POST",
        url: "/getpostdata/",
        data: {
            username: serpes_User,
        },
        headers: {
            "X-CSRFToken": getCookie('csrftoken') 
        },
       }).done(function(response){
        let datas=JSON.parse(response)
        renderposts(datas)
        
       })
    }

    function renderposts(next){

        next.forEach(function(next){
            nextx=next.fields
            let Pid=next.pk
            let likedornot = nextx.likedornot === "yes";
            let flwchak = nextx.flwOrNot === "yes";
            let btnf = nextx.btnc === "False";

            $("#responseposts").append(`
            <br>
            <div class="card gedf-card">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="mr-2">
                                <img width="45" src="media/${nextx.user_image}" alt="" style="border-radius: 50px; margin-right: 15px;">
                            </div>
                            <div class="ml-2">
                            
                            <form class="PostFlwForm" id="${Pid}" method="post" action="javascript:void(0)">
                                <a href="/userdetailedpost/${nextx.user_name}" style="text-decoration: none; color: black;">
                                    <div class="h5 m-0 d-inline-flex align-items-center" id="post-main-div">
                                        ${flwchak ? `<input type="hidden"  class="FlworNot${Pid}" value="yes">`:`<input type="hidden"  class="FlworNot${Pid}" value="no">`}

                                        <p class="post-username" id="PostFlwFormUsername${Pid}">@${nextx.user_name}</p>
                                        
                                                ${btnf ? `<button id="FlButton${Pid}" type="submit" 
                                                class="btn btn-outline-dark btn-sm ms-2" 
                                                data-mdb-button-init data-mdb-ripple-init 
                                                data-mdb-ripple-color="dark" 
                                                style="z-index: 1;">  ${flwchak ? `Followed`:`Follow`}  </button>`:  ``}
                                            
                                    </div>
                                </a>
                                </form>
                                <input type="hidden" class="FlworNot" value="{% if flwData.flwOrNot %}{{flwData.flwOrNot}}{% else %}no{% endif %}">

                                <div class="h7 text-muted">${nextx.first_name} ${nextx.last_name}</div>
                            </div>
                        </div>
                        <div></div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-body">
                        <p class="card-text"><small class="text-muted">${nextx.post_up_date}</small></p>
                        <br>
                        <p class="card-text">${nextx.post_txt}</p>
                    </div>
                    <img src="/media/${nextx.post_image}" class="card-img-bottom" alt="" style="border-radius: 5px;">
                </div>

                <div class="card-footer post-actions">

                <form class="PostForm" id="${Pid}" method="post" action="javascript:void(0)">
                    <input type="hidden"  class="LorNot${Pid}" value="${nextx.likedornot}">
                    <input type="hidden"  class="numoflike${Pid}" value="${nextx.num_of_likes}">

                <div id = "main_form${Pid}">
                    ${likedornot ? `
                <a href="javascript:void(0)" class="likeDislikeBtn${nextx.Pid}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                    </svg>Dislike${nextx.num_of_likes}
                </a>
                ` : `
                <a href="javascript:void(0)" class="likeDislikeBtn${nextx.Pid}">
                    <svg class="liked" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                        <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"/>
                      </svg>Like${nextx.num_of_likes}
                </a>
                `}
            </div>
            </form>
                    <a href="/detailedpost/${nextx.post_slug}" class="comment"><i class="fa fa-comment"></i> Comment</a>
                    <a href="javascript:void(0)" class="share"><i class="fa fa-share"></i> Share</a>
                </div>
            </div>
            `);

        })
    }
    }



    $(document).on('click', '.PostForm', function(event) {
            event.preventDefault();
            let form_id = $(this).attr('id');
            let serpes_User = $(".sr").val()
            let post_like_or_not=$(".LorNot"+form_id).val()
            let numlikes= parseInt($(".numoflike" + form_id).val())

            if (post_like_or_not==="no"){
                numlikes=numlikes+1
                $(".LorNot"+form_id).val("yes")
                document.querySelectorAll("#main_form"+form_id).forEach(function(e){
                    e.innerHTML=`
                    <a href="javascript:void(0)" class="likeDislikeBtn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                        </svg>Dislike ${numlikes}
                    </a>
                    `
                })
                
                
                $.ajax({
                    method:"POST",
                    url: "/like/",
                    data:{
                        "user_name":serpes_User,
                        "post_id_unique":form_id,
                    },
                    headers:{
                        "X-CSRFToken": getCookie("csrftoken"),
                    }
                    
                });
                
            }else{
                $(".LorNot"+form_id).val("no")
                document.querySelectorAll("#main_form"+form_id).forEach(function(e){
                    e.innerHTML=`
                    <a href="javascript:void(0)" class="likeDislikeBtn">
                    <svg class="liked" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                        <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"/>
                      </svg>Like ${numlikes}
                    </a>
                    `
                })
                $.ajax({
                    method:"POST",
                    url: "/removelike/",
                    data:{
                        "user_name":serpes_User,
                        "post_id_unique":form_id,
                    },
                    headers:{
                        "X-CSRFToken": getCookie("csrftoken"),
                    }
                    
                });

                
            }

        })


    window.onload =function(){
        dataLoad()
    }


    window.onscroll = function() {
        dataLoad()
    };

    $(document).off("click", ".share").on("click", ".share", function(){
        let postslugx;
        postslugx = $(".Pslx").val();
        let linkToCopy=`http://127.0.0.1:8000/detailedpost/${postslugx}`
    
        navigator.clipboard.writeText(linkToCopy)
    })



    $(document).on('submit', '.PostFlwForm', function() {
        event.preventDefault();

        let flwingUser=$(".sr").val()
        let flwedUserID=$(this).attr("id")
        let flwedusername = $(`#PostFlwFormUsername${flwedUserID}`).text()
        flwedusername=flwedusername.replace("@","")
        console.log(flwedUserID)
        console.log(flwedusername)
        let flwornot=$(`.FlworNot${flwedUserID}`).val()
        console.log(flwornot)

        
        if (flwornot==="no"){
            $(`#FlButton${flwedUserID}`).text("Followed")
            $.ajax({
                method:"POST",
                url:"/dofollow/",
                data:{
                    "following_user":flwingUser,
                    "followed_user":flwedusername,
                    "flwstatus":flwornot,
                },
                headers:{
                    "X-CSRFToken": getCookie("csrftoken"),
                    
                },
                
            }).done(
                function(){
                    $(`.FlworNot${flwedUserID}`).val("yes")
                }
            )
            
        }else{
            $(`#FlButton${flwedUserID}`).text("Follow")
            $.ajax({
                method:"POST",
                url:"/dofollow/",
                data:{
                    "following_user":flwingUser,
                    "followed_user":flwedusername,
                    "flwstatus":flwornot,
                },
                headers:{
                    "X-CSRFToken": getCookie("csrftoken"),
    
                },
            
            }).done(
                function(){
                    $(`.FlworNot${flwedUserID}`).val("no")
                }
            )
        }

    })

        
