import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  #移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  #初期値:画面内
    if rct.left < 0 or WIDTH < rct.right :
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate  #横方向、縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    引数：スクリーンの大きさ
    戻り値：なし
    こうかとんと爆弾が触れたらゲームオーバーの画面を表示する
    """
    bl_img = pg.Surface((WIDTH, HEIGHT))  #四角形のSurfaceを作る
    pg.Rect(0, 0, WIDTH, HEIGHT)  #画面に四角を表示
    bl_img.set_alpha(200)
    screen.blit(bl_img, [0,0])

    fonto = pg.font.Font(None, 80)  #画面に文字を表示
    txt = fonto.render("Game Over" , True, (255, 255, 255))
    text_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(txt, text_rct)

    kk_over_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  #泣いてるこうかとんを表示
    screen.blit(kk_over_img, [text_rct[0]-75, text_rct[1]])
    screen.blit(kk_over_img, [text_rct[0]+325, text_rct[1]])
    pg.display.update()

    time.sleep(5)  #画面を５秒停止


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：こうかとんの大きさのリストと速さのリスト
    時間経過で大きさと速さが変更される
    """
    bb_accs = [a for a in range(1, 11)]  #加速度の設定
    bb_img_lst = []
    for r in range(1, 11):  #大きさの設定
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_img_lst.append(bb_img)  #大きさをlistに格納
    return bb_accs, bb_img_lst


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    引数：進む向き
    戻り値：こうかとんの向き
    進む方向にこうかとんが向く
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    if sum_mv[0] != 0 and sum_mv[1] != 0:
        kk_img = pg.transform.rotozoom(kk_img, 45, 1.0)
    if sum_mv[0] == 0 and sum_mv[1] != 0:
        kk_img = pg.transform.rotozoom(kk_img, 90, 1.0)
    if sum_mv[0] == -5:
        kk_img = pg.transform.flip(kk_img, True, False)
    return kk_img




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # bb_img = pg.Surface((20,20))  #一辺が20の正方形Surfaceを作る
    # pg.draw.circle(bb_img,(255,0,0),(10,10),10)  #赤い円を描く
    # bb_img.set_colorkey((0,0,0))  #黒を透明にする
    vx, vy = +5, +5
    tmr = 0
    bb_accs, bb_imgs = init_bb_imgs()
    avx = vx*bb_accs[min(tmr//500, 9)]  #爆弾の速さのlistから値をとる
    bb_img = bb_imgs[min(tmr//500, 9)]  #爆弾の大きさのlistから値をとる
    bb_rct = bb_img.get_rect()  #爆弾のRectを取得
    bb_rct.centerx = random.randint(0,WIDTH)  #爆弾の横座標 
    bb_rct.centery = random.randint(0,HEIGHT)  #爆弾の縦座標
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  #こうかとんRectと爆弾Rectの衝突判定
            gameover(screen)  #ゲームオーバーの文字を画面に表示
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
            vx, vy = get_kk_img(tuple(sum_mv))

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #移動を無かったことにする
        screen.blit(kk_img, kk_rct)
        avx = vx*bb_accs[min(tmr//500, 9)]  #爆弾の速さのlistから値をとる
        bb_img = bb_imgs[min(tmr//500, 9)]  #爆弾の大きさのlistから値をとる
        bb_rct.width  #爆弾の横幅を変更
        bb_rct.height  #爆弾の高さを変更
        bb_rct.move_ip(avx, vy) #爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #横方向にはみ出ていたら
            vx *= -1
        if not tate:  #縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  #爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
