# shadingCorrection_MoveStage

先执行宏mac文件，会生成shadingSample.txt。这是多点地图，目前是3x3, 顺序是x,y,z(亮度)
然后执行surfacefit_for_shading.exe,会生成shadingCorrection.tif
setup.py是python 3.5版下的编译说明。在win10 64位下测试通过。
