from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse
from data.models import SBUser,UserPost,LikeOfUser,CommentsOfUser,UserFollowData,UserMessageData,VoiceMessage
import random
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import json
from django.core import serializers
from itertools import chain

def home(request):
    log = request.session.get("log")
    if log:
        profile_image = request.session.get('profile_image')
        Username = request.session.get("username")
        DitalsOfUser=SBUser.objects.get(user_name=Username)
        SB_posts_for_user = UserPost.objects.all().order_by('?')[:3]
        
        ele={
            "log":log,
            "UserData": DitalsOfUser,
            "pots": SB_posts_for_user,
            "surpesUser":Username,
            "PostData":DitalsOfUser,
            
        }
        return render(request, 'home.html',ele)
    elif request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if SBUser.objects.filter(user_name=username,password=password).exists():
            User_data=SBUser.objects.get(user_name=username,password=password)
            request.session['log'] = True
            request.session['first_name'] = User_data.fname
            request.session['last_name'] = User_data.lname
            request.session['username'] = User_data.user_name
            request.session['dob'] = User_data.dateOfBirthOfUser
            request.session['email'] = User_data.email
            request.session['password'] = User_data.password
            return redirect("/")
        else:
            ele={
                "error":True,
            }
            return render(request, 'home.html',ele)
        
        
    return render(request, 'home.html')
def signin(request):
    if request.method=="POST":
        fname=request.POST.get("first_name")
        lname=request.POST.get("last_name")
        uname=request.POST.get("username")
        dateOfBirth=request.POST.get("dob")
        Uemail=request.POST.get("email")
        password=request.POST.get("password")
        pro_image=request.FILES.get("profile_image")
        
        code=random.randint(111111, 999999)
        
        if pro_image:
            fs = FileSystemStorage()
            filename = fs.save(pro_image.name, pro_image)
            uploaded_file_url = filename
            
        request.session['log'] = True
        request.session['first_name'] = fname
        request.session['last_name'] = lname
        request.session['username'] = uname
        request.session['dob'] = dateOfBirth
        request.session['email'] = Uemail
        request.session['password'] = password
        request.session['profile_image'] = uploaded_file_url
        request.session['verification_code'] = code
        
        
        subject = "Bro's Book Email Verification."
        message = f'''
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <h1 style="text-align: center; color: #4a76a8;">Bro's Book Email Verification</h1>
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #4a76a8; text-align: center;">Verify Your Email Address</h2>
                <p>Hi <strong>{fname} {lname}</strong>,</p>
                <p>Thank you for joining Bro's Book! Please use the verification code below to verify your email address:</p>
                
                <div style="text-align: center; margin: 20px 0;">
                    <p style="background-color: #f3f3f3; padding: 15px; border-left: 4px solid #4a76a8; font-size: 24px; font-weight: bold; letter-spacing: 5px;">
                        {code}
                    </p>
                </div>
                
                <p style="text-align: center;">If you didn’t sign up for Bro's Book, you can safely ignore this email.</p>
                <p style="text-align: center;">This code will expire in 30 minutes.</p>
                
                <hr style="border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="text-align: center; font-size: 12px; color: #888;">This is an automated email from Bro's Book. Please do not reply.</p>
            </div>
        </body>
        </html>
        '''


        email_from = 'therayhan009@gmail.com'
        recipient_list = [Uemail]
        email = EmailMultiAlternatives(subject, strip_tags(message), email_from, recipient_list)
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)

        
        return redirect("/emailverification/")
        
    return render(request, 'signin.html')

def addpost(request):
    log = request.session.get("log")
    if log:
        if request.method=="POST":
            fname = request.session.get('first_name')
            lanme = request.session.get('last_name')
            username = request.session.get('username')
            profile_image = request.session.get('profile_image')
            User_data=SBUser.objects.get(user_name=username)
            post_txt = request.POST.get('post_text')
            post_img = request.FILES.get('post_image')
            
            if post_img:
                data=UserPost(
                    first_name=fname,
                    last_name=lanme,
                    user_name=username,
                    post_txt=post_txt,
                    user_image=User_data.profileImage,
                    post_image=post_img,
                )
                
            else:
                data=UserPost(
                    first_name=fname,
                    last_name=lanme,
                    user_name=username,
                    post_txt=post_txt,
                    user_image=User_data.profileImage,
                )
            data.save()

            return JsonResponse({
                "msg":"sended!! saved on Models"
            })
        #     fname = request.session.get('first_name')
        #     lanme = request.session.get('last_name')
        #     username = request.session.get('username')
        #     profile_image = request.session.get('profile_image')
        #     password = request.session.get('password')
            
        #     post_txt=request.POST.get("post_text")
        #     post_img=request.FILES.get("post_image")
            
        #     User_data=SBUser.objects.get(user_name=username,password=password)
            
        #     if post_img:
        #         data=UserPost(
        #             first_name=fname,
        #             last_name=lanme,
        #             user_name=username,
        #             post_txt=post_txt,
        #             user_image=User_data.profileImage,
        #             post_image=post_img,
        #         )
                
        #     else:
        #         data=UserPost(
        #             first_name=fname,
        #             last_name=lanme,
        #             user_name=username,
        #             post_txt=post_txt,
        #             user_image=User_data.profileImage,
        #         )
        #     data.save()
        #     return redirect("/")
        else:
            username = request.session.get('username')
            UserData=SBUser.objects.get(user_name=username)
            ele={
                "log":log,
                "UserData":UserData,
            }
            return render(request,"addpost.html",ele)
    
    else:
        return redirect("/signin/")
    

        

def emailverification(request):
    if request.method=="POST":
        enterdCode=request.POST.get("verification_code")
        code=request.session.get("verification_code")
        if str(enterdCode)==str(code):
            del request.session["verification_code"]
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            username = request.session.get('username')
            dob = request.session.get('dob')
            email = request.session.get('email')
            password = request.session.get('password')
            profile_image = request.session.get('profile_image')
            
            data=SBUser(
                fname=first_name,
                lname=last_name,
                email=email,
                user_name=username,
                password=password,
                dateOfBirthOfUser=dob,
                profileImage=profile_image
            )
            data.save()
            return redirect("/")
    return render(request,"email_verification.html")


def profile(request):
    username = request.session.get('username')
    User_data=SBUser.objects.get(user_name=username)
    user_posts=UserPost.objects.filter(user_name=username)[::-1]
    num_of_post=len(UserPost.objects.filter(user_name=username))
    ele={
        "log":True,
        "Udata":User_data,
        "pots":user_posts,
        "UserData":User_data,
        "postlen":num_of_post,
        "surpesUser":username,
        }
    return render(request,"profile.html",ele)

def getprofileposts(request):
    if request.method == "POST":
        username = request.POST.get('username')
        SB_posts_for_user = UserPost.objects.filter(user_name=username)[::-1]
        data = serializers.serialize(
            "json", 
            SB_posts_for_user, 
        )
        datax= json.loads(data)
        
        
        for obj in datax:
            po = obj['pk']
            chak_like = LikeOfUser.objects.filter(user_name_Of_liked_user=username,liked_post_id = po)
            chak_like_num = LikeOfUser.objects.filter(liked_post_id = po)
            num_of_likes=len(chak_like_num)
            # print(num_of_likes)
            if chak_like:
                obj['fields']['likedornot'] = "yes"
            else:
                obj['fields']['likedornot'] = "no"
            obj['fields']['num_of_likes']=num_of_likes
                
        newdata=json.dumps(datax)
        
        finaldata = newdata.replace('"', '\"')
        # finaldata = json.loads(newdata)
        
        return JsonResponse(finaldata , safe=False)
    

def logout(request):
    request.session.flush()
    return redirect("/")


def getpostdata(request):
    if request.method == "POST":
        SB_posts_for_user = UserPost.objects.all().order_by('?')[:3]
        data = serializers.serialize(
            "json", 
            SB_posts_for_user, 
        )
        datax= json.loads(data)
        
        username = request.POST.get('username')
        
        for obj in datax:
            po = obj['pk']
            posttt=UserPost.objects.get(id=po)
            postUPusername=posttt.user_name
           
            chak_like = LikeOfUser.objects.filter(user_name_Of_liked_user=username,liked_post_id = po)
            chak_like_num = LikeOfUser.objects.filter(liked_post_id = po)
            num_of_likes=len(chak_like_num)
            # print(num_of_likes)
            if chak_like:
                obj['fields']['likedornot'] = "yes"
            else:
                obj['fields']['likedornot'] = "no"
            obj['fields']['num_of_likes']=num_of_likes
            try:
                if username==postUPusername:
                    obj['fields']['flwOrNot']="False"
                    obj['fields']['btnc']="True"
                else:
                    Uflwornot=UserFollowData.objects.get(following_user=username,followed_user=postUPusername)
                    obj['fields']['flwOrNot']=Uflwornot.flwOrNot
                    obj['fields']['btnc']="False"
            except:
                obj['fields']['flwOrNot']="False"
                obj['fields']['btnc']="False"
           
                
        newdata=json.dumps(datax)
        
        finaldata = newdata.replace('"', '\"')
        # finaldata = json.loads(newdata)
        
        return JsonResponse(finaldata , safe=False)
    
    
    
def like(request):
    if request.method == "POST":
        u=request.POST.get("user_name")
        
        pid=request.POST.get("post_id_unique")
        
        data=LikeOfUser(
            user_name_Of_liked_user=u,
            liked_post_id=pid,
        )
        data.save()
        return JsonResponse({
            "msg":"ok!"
        })
    
def removelike(request):
    if request.method == "POST":
        u=request.POST.get("user_name")
        
        pid=request.POST.get("post_id_unique")

        data=LikeOfUser.objects.get(user_name_Of_liked_user=u,liked_post_id=pid)
        data.delete()
        return JsonResponse({
            "msg":"ok!"
        })  
    
def dislike(request):
    if request.method == "GET":
        SB_posts_for_user = UserPost.objects.all().order_by('?')[:3]
        data = serializers.serialize("json",SB_posts_for_user)
        # data= json.loads(data)
        return JsonResponse(data , safe=False)
    
def detailedpost(request,link):
    log = request.session.get("log")
    if log:
        Username = request.session.get("username")
        DitalsOfUser=SBUser.objects.get(user_name=Username)
        rqPost=UserPost.objects.get(post_slug=link)
        ele={
            "log":log,
            "UserData": DitalsOfUser,
            "rqpost":rqPost,
            "rqpostid":rqPost.id,
            "surpesUser":Username,
            
        }
        return render(request, 'Dpost.html',ele)
    
    
    
def getcomments(request):
    if request.method == "POST":
        postid=request.POST.get("postid")
        serpes_user=request.POST.get("sr")
        print(postid)
        commented_post_data=CommentsOfUser.objects.filter(commented_post_id=postid)
        serpes_user_data=SBUser.objects.get(User_name=serpes_user)
        final_data = serializers.serialize('json',commented_post_data,serpes_user_data)
        
        user_info = {
            # 'username': serpes_user_data.user_name,
            'proImage': serpes_user_data.profileImage,
        }

        response_data = {
            'comments': final_data,
            'user_info': user_info,
        }
        print(response_data)
        
        return JsonResponse(response_data,safe=False)
    
def addcomments(request):
    if request.method == "POST":
        postid=request.POST.get("postid")
        comTxt=request.POST.get("comment_txt")
        serpes_user=request.POST.get("sr")
        data=CommentsOfUser(
            user_name_Of_liked_user= serpes_user ,
            commented_post_id= postid,
            comment_txt=comTxt,
        )
        data.save()
        
        return JsonResponse(
            {"msg":"ok!"}
        )
        
        
def userdetailedpost(request,link):
    log = request.session.get("log")
    Username = request.session.get("username")
    if link==Username:
        return redirect("/profile/")
    try:
        flw = UserFollowData.objects.get(following_user=Username, followed_user=link)
    except UserFollowData.DoesNotExist:
        flw = False
    DitalsOfUser=SBUser.objects.get(user_name=Username)
    requested_profile_user_data=SBUser.objects.get(user_name=link)
    postCount=len(UserPost.objects.filter(user_name=link))
    if log:
        ele={
            "log":True,
            "Udata": requested_profile_user_data,
            "SRUserData":DitalsOfUser,
            "postlen":postCount,
            "UserData":DitalsOfUser,
            "flwData":flw,
            }
    else:
        ele={
            "Udata": requested_profile_user_data,
            "postlen":postCount,
            
            }
    return render(request, 'UserProfile.html',ele)


def dofollow(request):
    flwingUser=request.POST.get("following_user")
    flwedUser=request.POST.get("followed_user")
    flw_status=request.POST.get("flwstatus")
    print(flw_status)
    try:
        x = UserFollowData.objects.get(following_user=flwingUser, followed_user=flwedUser)
        print("UUUUUUUUU")
        if flw_status=="no":
            x.flwOrNot = "yes" 
        else:
            x.flwOrNot = "no"
        x.save()
    except:
        UserFollowData.objects.create(
            following_user=flwingUser,
            followed_user=flwedUser,
            flwOrNot="yes", 
        )
    
    return JsonResponse({
        "msg":"ok"
    })


def friends(request):
    log = request.session.get("log")
    Username = request.session.get("username")
    #  profile_image = request.session.get('profile_image')
    # Username = request.session.get("username")
    DitalsOfUser=SBUser.objects.get(user_name=Username)
    # SB_posts_for_user = UserPost.objects.all().order_by('?')[:3]
    ele={
        "log":log,
        "srUser":Username,
        "UserData": DitalsOfUser,
        "PostData":DitalsOfUser,
        
    }
    return render(request,"friends.html",ele)


def getuserfollowers(request):
    if request.method == "GET":
        srusername= request.GET.get("Quser")
        data=UserFollowData.objects.filter(followed_user=srusername)
        l=[]
        for i in data:
            if i.flwOrNot=="yes":
                l.append(i)
        sdata=serializers.serialize("json",l)
        
        return JsonResponse(sdata,safe=False)
    
def getuserfollowerinfo(request):
    if request.method == "GET":
        srusername= request.GET.get("Quser")
        data=SBUser.objects.filter(user_name=srusername)
        # print(data)
        sdata=serializers.serialize("json",data)
        
        return JsonResponse(sdata,safe=False)
def getuserfollow(request):
    if request.method == "GET":
        srusername= request.GET.get("Quser")
        
        data=UserFollowData.objects.filter(following_user=srusername)
        
        l=[]
        for i in data:
            if i.flwOrNot=="yes":
                l.append(i)
                
        sdata=serializers.serialize("json",l)
        
        return JsonResponse(sdata,safe=False)
    
def getuserfollowinfo(request):
    if request.method == "GET":
        srusername= request.GET.get("Quser")
        data=SBUser.objects.filter(user_name=srusername)
        # print(data)
        sdata=serializers.serialize("json",data)
        
        return JsonResponse(sdata,safe=False)
    
    
def getuserfriends(request):
    if request.method == "GET":
        srusername= request.GET.get("Quser")
        
        data=UserFollowData.objects.filter(following_user=srusername)
        l=[]
        for i in data:
            if UserFollowData.objects.filter(following_user=i.followed_user , followed_user=i.following_user).exists():
                if UserFollowData.objects.get(following_user=i.followed_user , followed_user=i.following_user).flwOrNot=="yes" and UserFollowData.objects.get(following_user=i.following_user , followed_user=i.followed_user).flwOrNot=="yes":
                    l.append(i)
            
        print(l)
        sdata=serializers.serialize("json",l)
        # print(sdata)
        
        
        return JsonResponse(sdata,safe=False)
    
def getuserfriendsinfo(request):    
    if request.method == "GET":
        Quser= request.GET.get("Quser")
        data=SBUser.objects.filter(user_name=Quser)
        # print(data)
        sdata=serializers.serialize("json",data)
        
        return JsonResponse(sdata,safe=False)
    message
def inbox(request):    
    log = request.session.get("log")
    Username = request.session.get("username")
    if log:
        ele={
            "log":log,
            "username":Username
        }
        return render(request,"messageing.html",ele)
    return HttpResponse("404")


def message(request,link):  
    log = request.session.get("log")
    Username = request.session.get("username")
    cr_data=SBUser.objects.get(user_name=link)
    if log:
        ele={
            "log":log,
            "username":Username,
            "chtangUser":link,
            "chtangUserData":cr_data,
        }
        return render(request,"Dmessages.html",ele)
    return HttpResponse("404")

def getmessage(request):    
    sr_user=request.GET.get("user")
    chat_user=request.GET.get("chtangUser")
    
    user_M=UserMessageData.objects.filter(message_from=sr_user , message_to=chat_user)
    chat_user_M=UserMessageData.objects.filter(message_from=chat_user ,message_to=sr_user)
    user_V_M=VoiceMessage.objects.filter(V_message_from=sr_user , V_message_to=chat_user)
    chat_user_V_M=VoiceMessage.objects.filter(V_message_from=chat_user ,V_message_to=sr_user)
    
    main_data = list(chain(user_M, chat_user_M, user_V_M, chat_user_V_M))
    
    main_data = sorted(main_data, key=lambda x: x.sno_of_message)
    
    # print(main_data.order_by("sno_of_message"))
    
    final_data=serializers.serialize("json",main_data)
    # print(final_data)
    
    return JsonResponse(final_data,safe=False)
    
    
def sendmessage(request):
    sr_user=request.GET.get("user")
    chat_user=request.GET.get("chtangUser")
    message=request.GET.get("message")
    print(message)
    
    data=UserMessageData.objects.create(
        message_from=sr_user,
        message_to=chat_user,
        sent_message = message,
        sno_of_message=UserMessageData.objects.filter(message_from=sr_user,message_to=chat_user).count() + UserMessageData.objects.filter(message_from=chat_user,message_to=sr_user).count() + VoiceMessage.objects.filter(V_message_from=chat_user,V_message_to=sr_user).count() + VoiceMessage.objects.filter(V_message_from=sr_user,V_message_to=chat_user).count()
    )
    data.save()
    return JsonResponse({
        "msg":" ok!!"
    })
    
    
def uploadVmessage(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        sr_user = request.POST.get('sr_user')
        chat_user = request.POST.get('chat_user')
        
        data=VoiceMessage.objects.create(
            V_message_from=sr_user,
            V_message_to=chat_user,
            audio_file = audio_file,
            sno_of_message=UserMessageData.objects.filter(message_from=sr_user,message_to=chat_user).count() + UserMessageData.objects.filter(message_from=chat_user,message_to=sr_user).count() + VoiceMessage.objects.filter(V_message_from=chat_user,V_message_to=sr_user).count() + VoiceMessage.objects.filter(V_message_from=sr_user,V_message_to=chat_user).count()
        )
        data.save()
        
        return JsonResponse({
        "msg":" ok!!"
        })