import pygame as pg,sys
import random
import Asukamirai_function as asuka

pg.init()
screen = pg.display.set_mode((800,600))
##自機データ
myimg = pg.image.load("./image/Renjer(Blue).png")
myimg = pg.transform.scale(myimg,(50,50))
myrect = pg.Rect(400,500,50,50)
##弾データ
bulletimg = pg.image.load("./image/mybullet.tga")
bulletimg = pg.transform.scale(bulletimg,(50,50))
bulletrect=pg.Rect(400,-100,50,50)
##敵データ
emyimg = pg.image.load("./image/enemy1.tga")
emyimg = pg.transform.scale(emyimg,(50,50))
emyos = []
#UFOデータ
ufoimg = pg.image.load("./image/enemy1.tga")
ufoimg = pg.transform.scale(ufoimg,(50,50))
emyos = []
for i in range(10):
    ux = random.randint(0,800)
    uy = -100 * i
    emyos.append(pg.Rect(ux,uy,50,50))
##ボタンデータ
replay_img = pg.image.load("./image/btn006_08.gif")
##メインループ
pushFlag = False
page = 1
score = 0

##ボタンを押したら、newpageにジャンプする
def button_to_jump(btn,newpage):
    global page,pushFlag
    mdow = pg.mouse.get_pressed()
    (mx,my)=pg.mouse.get_pos()
    if mdow[0]:
        if btn.collidepoint(mx,my) and pushFlag == False:
            page = newpage
            pushFlag = True
        else:
            pushFlag = False
##ゲームステージ
def gamestage():
    ##画面の初期化
    global score
    global page
    screen.fill(pg.Color("BLACK"))
    ##ユーザーからの入力調べ
    (mx,my) = pg.mouse.get_pos()
    mdown = pg.mouse.get_pressed()
    #星の処理
    
    ##自機の処理ß
    myrect.x = mx -25
    screen.blit(myimg,myrect)
    ##弾の処理
    ##手順①

    if mdown[0] and bulletrect.y < 0:
        asuka.bullet(bulletrect,myrect)
    if bulletrect.y >= 0:
        asuka.bulletAftter(bulletimg,bulletrect,myrect,screen)

    ##敵の処理
    ##手順②
    for emy in emyos:
        emy.y += 10
        screen.blit(ufoimg,emy)
        if emy.colliderect(myrect):
            page = 2
        score = asuka.ufodisplay(emy,myrect,bulletrect,score,page)



    ##スコア処理
    #score = score + 10
    font = pg.font.Font(None,40)
    text = font.render("SCORE : "+ str(score),True,pg.Color("WHITE"))
    screen.blit(text,(20,20))

    ##データのリセット
def gamereset():
    global score
    score = 0
    myrect.x = 400
    myrect.y = 500
    bulletrect.y = -100
    for i in range (10):
        emyos[i] = pg.Rect(random.randint(0,800),-100 * i,50,50)
##ゲームオーバー
def gameover():
    screen.fill(pg.Color("NAVY"))
    font = pg.font.Font(None,150)
    text = font.render("GAMEOVER",True,pg.Color("RED"))
    screen.blit(text,(100,200))
    btn1 = screen.blit(replay_img,(320,400))
    font = pg.font.Font(None,40)
    text = font.render("SCORE : "+str(score),True,pg.Color("WHITE"))
    screen.blit(text,(20,20))
    button_to_jump(btn1,1)
    if page == 1:
        gamereset()

while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()

    pg.display.update()
    pg.time.Clock().tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()