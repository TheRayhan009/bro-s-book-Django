from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse
from data.models import SBUser,UserPost,LikeOfUser,CommentsOfUser
import random
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import json
from django.core import serializers

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

        User_data=SBUser.objects.get(user_name=username,password=password)
        
        if User_data:
            request.session['log'] = True
            request.session['first_name'] = User_data.fname
            request.session['last_name'] = User_data.lname
            request.session['username'] = User_data.user_name
            request.session['dob'] = User_data.dateOfBirthOfUser
            request.session['email'] = User_data.email
            request.session['password'] = User_data.password
            return redirect("/")
        
        
        
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
        
        
        final_data = serializers.serialize('json',commented_post_data)
        print(final_data)
        
        return JsonResponse(final_data,safe=False)
    
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