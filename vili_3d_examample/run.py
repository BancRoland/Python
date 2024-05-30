# pyinstaller --onefile --noconsole hanyatradar.py

import numpy as np
import os
import sys
from PySide6.QtCore import ( QPoint)
from PySide6.QtGui import (QPainter, qRgba, Qt, QPen, QFont, QColor )
from PySide6.QtWidgets import ( QPushButton, QApplication, QHBoxLayout, QGridLayout, QDialog, QFrame, QSlider, QLabel, QTabWidget, QWidget)

cColorGridBorder =    QColor(qRgba(0x00, 0x00, 0xF0, 0xff))
cColorGridMiddle =    QColor(qRgba(0x80, 0x80, 0xF0, 0xff))
cColorScUvCircle =    QColor(qRgba(0xF0, 0x80, 0x80, 0xff))
cColorAntenna    =    QColor(qRgba(0xF0, 0x40, 0x20, 0xff))
cColorScUvGridA   =    QColor(qRgba(0xC0, 0xC0, 0xC0, 0xff))
cColorScUvGridB   =    QColor(qRgba(0xC0, 0xF0, 0xC0, 0xff))


cNumOfUvGrids   = 20
cNumOfHorPoints = 16
cNumOfVerPoints = 10
BordeLines=np.zeros([cNumOfHorPoints,cNumOfVerPoints,3],dtype=float)

gAzimLimitDeg=45
gElevUpDeg=30
gElevDnDeg=-10
gRadarSupineDeg = 10

def WrUvStr(fff,ix,iy):
    fu, fv = Point2UVf(BordeLines[ix, iy])
    sx = "{:>10.6f},{:>+10.6f}\n".format(fu, fv)
    fff.write(sx)


def SaveBorder (sFileName):
    if os.path.exists(sFileName):
        fff= open(sFileName, "w")
    else:
        fff= open(sFileName, "x")
    iy=0
    for ix in range(cNumOfHorPoints):
        WrUvStr(fff, ix, iy)
    ix=cNumOfHorPoints-1
    for iy in range(cNumOfVerPoints):
        WrUvStr(fff, ix, iy)
    iy=cNumOfVerPoints-1
    for ix in range(cNumOfHorPoints-1,-1,-1):
        WrUvStr(fff, ix, iy)
    ix=0
    for iy in range(cNumOfVerPoints-1,-1,-1):
        WrUvStr(fff, ix, iy)
    fff.close()



def rot_mtx_yaw (yaw):
    x=np.zeros([3,3],dtype=float)
    x[0, 0] = np.cos(yaw)
    x[0, 1] =-np.sin(yaw)
    x[1, 1] = np.cos(yaw)
    x[1, 0] = np.sin(yaw)
    x[2, 2] = 1.0
    return (x)
def rot_mtx_pitch (pitch):
    x=np.zeros([3,3],dtype=float)
    x[0, 0] = np.cos(pitch)
    x[0, 2] = np.sin(pitch)
    x[1, 1] = 1.0
    x[2, 0] =-np.sin(pitch)
    x[2, 2] = np.cos(pitch)
    return (x)
def rot_mtx_roll (roll):
    x=np.zeros([3,3],dtype=float)
    x[0, 0] = 1.0
    x[1, 1] = np.cos(roll)
    x[1, 2] =-np.sin(roll)
    x[2, 1] = np.sin(roll)
    x[2, 2] = np.cos(roll)
    return (x)

def Polar2Descartes(pp):
    dp=np.empty(3,dtype=float)
    dp[0]=np.cos(pp[0])*np.sin(pp[1])
    dp[1]=np.cos(pp[0])*np.cos(pp[1])
    dp[2] = np.sin(pp[0])
    return dp

def InitBorderLines():
    pp = np.empty(2,dtype=float)
    for ix in range(cNumOfHorPoints):
        fx = (2 * ix - (cNumOfHorPoints - 1)) / (cNumOfHorPoints - 1)
        pp[1] = np.deg2rad(fx * gAzimLimitDeg)
        for iy in range(cNumOfVerPoints):
            fx = iy / (cNumOfVerPoints - 1)
            pp[0] = np.deg2rad(gElevDnDeg + fx * (gElevUpDeg - gElevDnDeg))
            BordeLines[ix,iy]=Polar2Descartes(pp)

########################################################################
def PutTextRot(mp,sx,sp,iAlpha):
    mp.save()
    mp.translate(sp)
    mp.rotate(iAlpha)
    mp.drawText(QPoint(0,0),sx)
    mp.restore()
def PointTrf (mps,iViewRotDeg,iViewElevDeg,fCameraDist):
    mpy = np.empty(3, dtype=float)
    mpx=np.empty(3,dtype=float)
    #
    c=np.cos(np.deg2rad(iViewRotDeg))
    s=np.sin(np.deg2rad(iViewRotDeg))
    mpx[0]=+mps[1]*c+mps[0]*s
    mpx[1]=-mps[1]*s+mps[0]*c
    mpx[2]=+mps[2]
    #
    c=np.cos(np.deg2rad(iViewElevDeg))
    s=np.sin(np.deg2rad(iViewElevDeg))
    mpy[0]=+mpx[0]
    mpy[1]=+mpx[1]*c+mpx[2]*s
    mpy[2]=-mpx[1]*s+mpx[2]*c
    #
    mpy[1]-=fCameraDist
    return  mpy

def ProjectPointFlt(mps,iViewRotDeg,iViewElevDeg,fCameraDist):
    xp = np.empty(2, dtype=float)
    mp=PointTrf(mps, iViewRotDeg, iViewElevDeg, fCameraDist)
    xp[0]=-mp[0]/mp[1]
    xp[1]= mp[2]/mp[1]
    return  xp

def ProjectPointQP(mps,iViewRotDeg,iViewElevDeg,fCameraDist,pCenter,fScale):
    xp = ProjectPointFlt(mps,iViewRotDeg,iViewElevDeg,fCameraDist)
    mp=PointTrf(mps, iViewRotDeg, iViewElevDeg, fCameraDist)
    xp[0]=-mp[0]/mp[1]
    xp[1]= mp[2]/mp[1]
    return  pCenter+QPoint(int(fScale*xp[0]),int(fScale*xp[1]))
def PutAxisLine (mp,ap,iViewRotDeg,iViewElevDeg,fCameraDist,pCenter,fScale,sx):
    ep = ProjectPointQP(ap,iViewRotDeg,iViewElevDeg,fCameraDist,pCenter,fScale)
    mp.drawLine(pCenter, ep)
    dx = ep.x() - pCenter.x()
    dy = ep.y() - pCenter.y()
    PutTextRot(mp, sx, ep , np.rad2deg(np.pi + np.arctan2(dy, dx)) )

def Point2UVSpare (pd,pCenter,idr):
    px=rot_mtx_roll(np.deg2rad(-gRadarSupineDeg)) @ pd
    # np.copyto(px,pd)
    el=np.arcsin(px[2])
    az=np.arccos(px[1]/np.sqrt(px[0]**2+px[1]**2))
    if (px[0]<0.0): az*=-1.0
    fu = np.cos(el) * np.sin(az)
    fv = np.sin(el)
    return QPoint(int(pCenter.x()+fu*idr),int(pCenter.y()-fv*idr))

def Point2UVf (pd):
    px=rot_mtx_roll(np.deg2rad(-gRadarSupineDeg)) @ pd
    el=np.arcsin(px[2])
    az=np.arccos(px[1]/np.sqrt(px[0]**2+px[1]**2))
    if (px[0]<0.0): az*=-1.0
    fu = np.cos(el) * np.sin(az)
    fv = np.sin(el)
    return fu,fv

def Point2UVp (pd,pCenter,idr):
    fu,fv=Point2UVf(pd)
    return QPoint(int(pCenter.x()+fu*idr),int(pCenter.y()-fv*idr))

class FrmLyt (QFrame):        # draws the layout of the UCA
    PrevPos=QPoint(-1,-1)
    iViewRotDeg=-30
    iViewElevDeg=25
    def paintEvent(self, event):
        # +++PAINTER, init painter of image
        mPainter = QPainter()
        mPainter.begin(self)
        ww=event.rect().width()
        wh=event.rect().height()
        mUsedFont=QFont('Courier New', 10)
        mPainter.setFont(mUsedFont)
        # calculate largest distance
        fLargestDistance=1.0
        #
        fScale=2.5*float(min(ww,wh)/2)
        fCameraDist=3.6*fLargestDistance
        fAxisLen=1.4*fLargestDistance
        pCenter=QPoint(int(ww/2),int(wh/2))
        PutAxisLine(mPainter,np.array([fAxisLen, 0.0, 0.0]), self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale, "x/E")
        PutAxisLine(mPainter,np.array([0.0,fAxisLen, 0.0]), self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale, "y/N")
        PutAxisLine(mPainter,np.array([0.0, 0.0,fAxisLen]), self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale, "z/U")
        #
        pc = np.zeros(3, dtype=float)
        pp = np.zeros(3, dtype=float)
        pa = np.zeros([4,3], dtype=float)
        AntSize=0.2
        mpen = QPen(cColorAntenna, 2)
        mPainter.setPen(mpen)
        pa[0,0] = AntSize
        pa[0,1] = AntSize * np.sin(np.deg2rad(gRadarSupineDeg))
        pa[0,2] = -AntSize * np.cos(np.deg2rad(gRadarSupineDeg))
        np.copyto(pa[1],pa[0])
        np.copyto(pa[2],pa[0])
        np.copyto(pa[3],pa[0])
        pa[2,0]*=-1.0
        pa[3,0]*=-1.0
        pa[1,1]*=-1.0
        pa[2,1]*=-1.0
        pa[1,2]*=-1.0
        pa[2,2]*=-1.0
        mPainter.drawLine(ProjectPointQP(pa[0], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale),
                          ProjectPointQP(pa[1], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale))
        mPainter.drawLine(ProjectPointQP(pa[1], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale),
                          ProjectPointQP(pa[2], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale))
        mPainter.drawLine(ProjectPointQP(pa[2], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale),
                          ProjectPointQP(pa[3], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale))
        mPainter.drawLine(ProjectPointQP(pa[3], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale),
                          ProjectPointQP(pa[0], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale))
        mPainter.drawLine(ProjectPointQP(pa[0], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale),
                          ProjectPointQP(pa[2], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale))
        mPainter.drawLine(ProjectPointQP(pa[1], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale),
                          ProjectPointQP(pa[3], self.iViewRotDeg, self.iViewElevDeg, fCameraDist, pCenter, fScale))
        #
        mpenB = QPen(cColorGridBorder, 2)
        mpenM = QPen(cColorGridMiddle, 1)
        for ix in range(cNumOfHorPoints):
            if (ix == 0) or (ix == (cNumOfHorPoints - 1)):
                mPainter.setPen(mpenB)
            else:
                mPainter.setPen(mpenM)
            for iy in range(cNumOfVerPoints):
                pc = ProjectPointQP(BordeLines[ix, iy], self.iViewRotDeg, self.iViewElevDeg, fCameraDist,
                                    pCenter, fScale)
                if (iy > 0):
                    mPainter.drawLine(pc, pp)
                pp = pc
        for iy in range(cNumOfVerPoints):
            if (iy == 0) or (iy == (cNumOfVerPoints - 1)):
                mPainter.setPen(mpenB)
            else:
                mPainter.setPen(mpenM)
            for ix in range(cNumOfHorPoints):
                pc = ProjectPointQP(BordeLines[ix, iy], self.iViewRotDeg, self.iViewElevDeg, fCameraDist,
                                    pCenter, fScale)
                if (ix > 0):
                    mPainter.drawLine(pc, pp)
                pp = pc

        mPainter.end()
# mousePressEvent() , mouseReleaseEvent()
    def mousePressEvent(self, event):
        self.PrevPos=QPoint(event.position().x(),event.position().y())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.PrevPos = QPoint(-1, -1)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.PrevPos.x()!=-1:
            if (self.PrevPos.x()<event.position().x()): self.iViewRotDeg +=2
            if (self.PrevPos.x()>event.position().x()): self.iViewRotDeg -=2
            if (self.PrevPos.y()>event.position().y()): self.iViewElevDeg-=2
            if (self.PrevPos.y()<event.position().y()): self.iViewElevDeg+=2
            self.iViewRotDeg=max(-180,min(180,self.iViewRotDeg))
            self.iViewElevDeg=max(-90,min(90,self.iViewElevDeg))
        self.PrevPos = QPoint(event.position().x(), event.position().y())
        super().mouseMoveEvent(event)
        self.repaint()  # self.update()
# end of UcaLytFrm

class FrmUV (QFrame):        # draws the layout of the UCA
    def paintEvent(self, event):
        # +++PAINTER, init painter of image
        mPainter = QPainter()
        mPainter.begin(self)
        ww=event.rect().width()
        wh=event.rect().height()
        mUsedFont=QFont('Courier New', 10)
        mPainter.setFont(mUsedFont)
        #
        pCenter=QPoint(int(ww/2),int(wh/2))
        idr=int((min(ww,wh)/2)-2)
        mPainter.drawRect(pCenter.x()-idr,pCenter.y()-idr,2*idr,2*idr)
        #
        mpen = QPen(cColorScUvCircle, 1)
        mPainter.setPen(mpen)
        mPainter.drawEllipse(pCenter,idr,idr)
        #
        mpenA = QPen(cColorScUvGridA, 2)
        mpenB = QPen(cColorScUvGridB, 1)
        for i in range(cNumOfUvGrids-1):
            if (i%5==4):
                mPainter.setPen(mpenA)
            else:
                mPainter.setPen(mpenB)
            ix=int(2.0*idr*(0.5-(i+1)/cNumOfUvGrids))
            mPainter.drawLine(pCenter+QPoint(ix,1-idr),pCenter+QPoint(ix,idr-1))
            mPainter.drawLine(pCenter+QPoint(1-idr,ix),pCenter+QPoint(idr-1,ix))


        #
        mpenB = QPen(cColorGridBorder, 2)
        mpenM = QPen(cColorGridMiddle, 1)
        for ix in range(cNumOfHorPoints):
            if (ix == 0) or (ix == (cNumOfHorPoints - 1)):
                mPainter.setPen(mpenB)
            else:
                mPainter.setPen(mpenM)
            for iy in range(cNumOfVerPoints):
                pc = Point2UVp(BordeLines[ix, iy], pCenter, idr)
                if (iy>0):
                    mPainter.drawLine(pc, pp)
                pp=pc
        for iy in range(cNumOfVerPoints):
            if (iy == 0) or (iy == (cNumOfVerPoints - 1)):
                mPainter.setPen(mpenB)
            else:
                mPainter.setPen(mpenM)
            for ix in range(cNumOfHorPoints):
                pc = Point2UVp(BordeLines[ix, iy], pCenter, idr)
                if (ix > 0):
                    mPainter.drawLine(pc, pp)
                pp = pc


        #
        mPainter.end()

"""
gAzimLimitDeg=45
gElevUpDeg=30
gElevDnDeg=-10
gRadarSupineDeg = 10
"""

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)

        self.mFrmLyt = FrmLyt()
        self.mFrmUV = FrmUV()
        mLeftPanel=QTabWidget()
        mLeftPanel.addTab(self.mFrmLyt, 'layout')
        mLeftPanel.addTab(self.mFrmUV, 'U-V')

        # azimut limits
        self.mTxtAzimLimitDeg  = QLabel("azim:", self)
        self.mSldrAzimLimitDeg = QSlider(Qt.Orientation.Horizontal)
        self.mSldrAzimLimitDeg.setPageStep(1)
        self.mSldrAzimLimitDeg.setRange(0,90)
        self.mSldrAzimLimitDeg.setValue(gAzimLimitDeg)
        # elevation, upper
        self.mTxtElevUpDeg  = QLabel("elevu:", self)
        self.mSldrElevUpDeg = QSlider(Qt.Orientation.Horizontal)
        self.mSldrElevUpDeg.setPageStep(1)
        self.mSldrElevUpDeg.setRange(0,90)
        self.mSldrElevUpDeg.setValue(gElevUpDeg)
        # elevation, lower
        self.mTxtElevDnDeg  = QLabel("elevu:", self)
        self.mSldrElevDnDeg = QSlider(Qt.Orientation.Horizontal)
        self.mSldrElevDnDeg.setPageStep(1)
        self.mSldrElevDnDeg.setRange(0,90)
        self.mSldrElevDnDeg.setValue(-gElevDnDeg)
        # gRadarSupineDeg
        self.mTxtRadarSupineDeg  = QLabel("radarsup:", self)
        self.mSldrRadarSupineDeg = QSlider(Qt.Orientation.Horizontal)
        self.mSldrRadarSupineDeg.setPageStep(1)
        self.mSldrRadarSupineDeg.setRange(0,90)
        self.mSldrRadarSupineDeg.setValue(gRadarSupineDeg)
        #
        mExitButton = QPushButton("exit")



        mRightPanelLyt = QGridLayout()
        # cpi file, 0,1
        mRightPanelLyt.addWidget(self.mTxtAzimLimitDeg, 0,0)
        mRightPanelLyt.addWidget(self.mSldrAzimLimitDeg, 1,0)
        mRightPanelLyt.addWidget(self.mTxtElevUpDeg, 2,0)
        mRightPanelLyt.addWidget(self.mSldrElevUpDeg, 3,0)
        mRightPanelLyt.addWidget(self.mTxtElevDnDeg, 4,0)
        mRightPanelLyt.addWidget(self.mSldrElevDnDeg, 5,0)
        mRightPanelLyt.addWidget(self.mTxtRadarSupineDeg, 6,0)
        mRightPanelLyt.addWidget(self.mSldrRadarSupineDeg, 7,0)
        mRightPanelLyt.addWidget(mExitButton, 8, 0)


        mRightPanel = QWidget()
        mRightPanel.setLayout(mRightPanelLyt)

        mMainLayout = QHBoxLayout()
        mMainLayout.addWidget(mLeftPanel)
        mMainLayout.addWidget(mRightPanel)
        mMainLayout.setStretchFactor(mLeftPanel, 2)
        mMainLayout.setStretchFactor(mRightPanel, 1)

        self.setLayout(mMainLayout)

        # +++ connect
        self.mSldrAzimLimitDeg.valueChanged.connect(self.mUpdateAzimLimitDeg)
        self.mSldrElevUpDeg.valueChanged.connect(self.mUpdateElevUpDeg)
        self.mSldrElevDnDeg.valueChanged.connect(self.mUpdateElevDnDeg)
        self.mSldrRadarSupineDeg.valueChanged.connect(self.mUpdateRadarSupineDeg)
        mExitButton.clicked.connect(self.MyExitButtonFunc)
        # synchronize
        self.mUpdateAzimLimitDeg()
        self.mUpdateElevUpDeg()
        self.mUpdateElevDnDeg()
        self.mUpdateRadarSupineDeg()

    def mUpdateAzimLimitDeg(self):
        global gAzimLimitDeg
        gAzimLimitDeg=self.mSldrAzimLimitDeg.value()
        sx="azimut={}\u00B0".format(gAzimLimitDeg)
        self.mTxtAzimLimitDeg.setText(sx)
        InitBorderLines()
        self.repaint()          # self.update()
    def mUpdateElevUpDeg(self):
        global gElevUpDeg
        gElevUpDeg=self.mSldrElevUpDeg.value()
        sx="elev, upper={}\u00B0".format(gElevUpDeg)
        self.mTxtElevUpDeg.setText(sx)
        InitBorderLines()
        self.repaint()          # self.update()
    def mUpdateElevDnDeg(self):
        global gElevDnDeg
        gElevDnDeg=-self.mSldrElevDnDeg.value()
        sx="elev, lower={}\u00B0".format(gElevDnDeg)
        self.mTxtElevDnDeg.setText(sx)
        InitBorderLines()
        self.repaint()          # self.update()
    def mUpdateRadarSupineDeg(self):
        global gRadarSupineDeg
        gRadarSupineDeg=self.mSldrRadarSupineDeg.value()
        sx="radar supine={}\u00B0".format(gRadarSupineDeg)
        self.mTxtRadarSupineDeg.setText(sx)
        InitBorderLines()
        self.repaint()          # self.update()


    def MyExitButtonFunc(self):
        SaveBorder("BorderUVs.csv")
        self.close()

if __name__ == '__main__':
    InitBorderLines()
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())

