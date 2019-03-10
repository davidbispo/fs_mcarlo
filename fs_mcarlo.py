# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# fs_mcarlo
# Created on: 2018-05-12 16:35:25.00000
# by David Bispo Ferreira
# Description: O programa gera os arquivos necessarios para o calculo do fator de seguranca via taludes infinitos. Estes
# arquivos sao guardados num arquivo *.gdb do ArcGis, denominado "arquivo de parametros" ou "gdb de parametros".
# A partir de um gdb de parametros pode-se chamar o calculo de um fator de seguranca, ou de uma simulacao Monte Carlo 
# de cenarios. Veja a documentacao especifica de cada modulo para entender como funciona cada entrada. 

# O programa conta com tres modulos:
#
#1. Criacao de rasters com parametros padrao(criarasters_par)
#2. Simulacao de um fator de seguranca(calculaFS)
#3. Simulacao de multiplos fatores de seguranca e calculo das probabilidades(simulaFS)
#
#Coisas importantes:
#
#- Se der algum erro estranho, tente executar o gerenciador de tarefas: (CTRL+ALT+DEL), e feche os processos "ArcMap", "ArcGIS Connection" , "ArcGIS Cache manager"
#o spyder(caso esteja aberto) e os terminais python (pythonw.exe) que eventualmente estejam abertos
#
#- O Python e case-sensitive, isto e, ele entene letras maiusculas diferente de minusculas(i.e.:'True' eh diferente de 'true')
#
#- O programa pode ser rodado no terminal(fs_mcarlo) ou em um programa anaconda(fs_mcarlo_conda). A diferenca entre os 
#dois e' o archook, que busca as extensoes do arcpy para rodar no anaconda/spyder. 
#
#- No terminal digite: sys.path.append = r'pasta que voce colocou o codigo'. Na duvida, arraste do arccatalog para o terminal 
#para obter um endereco. o "r'" signigica raw string, isto e, que voce nao tem formatadores no texto. O unico jeito de passar
#enderecos sem usar duas barras(D://pasta//pasta2) e colocando esse r na frente da string. 
#
#- Importe o arcpy. Para definir o nomes de arquivos use strings, de preferencia passando nomes de 
#variaveis(e.g.: gdbpar = r'D:/folder/arquivo), e depois chame a funcao (e.g.:calculaFS(gdb_par))
#
#
#- No spyder, nao esqueca de instalar o archook. Abra seu anaconda prompt e digite "pip install archook"
#O arcpy nao e' compativel com o Anaconda, entao o archook deve ser inicializado para obtencao das bibliotecas pelo spyder.

# #---------------------------------------------------------------------------

# Importacao de modulos#

import os 
import arcpy
from arcpy import env
from arcpy.sa import *
import os
import numpy as np
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

###########################################################################################
################   CRIA RASTERS A PARTIR DA DEVLIVIDADE   #################################
def criarasters_par(sloperad, output_gdb_par,coes=True, coes_val=11, ang_at=True, ang_at_val=19, suct = True, suct_val = 2):
    """Cria os rasters de parametros, com saida em um gdb de parametros. """
   
    slope_rad = Raster(sloperad)
    path_slope = os.path.join(output_gdb_par,'slope_rad')
    slope_rad.save(path_slope)
    
    if coes == True: # se a flag de coesao for verdadeira, gera raster
        output_coes = os.path.join(output_gdb_par,'coes')
        COES = Raster(sloperad)*0+coes_val
        COES.save(output_coes)
    
    if ang_at == True:# se a flag de angulo de atrito for verdadeira, gera raster
         output_ang_at = os.path.join(output_gdb_par,'ang_at_rad')
         ang_at_rad = Raster(sloperad)*0+ang_at_val*3.14159/180
         ang_at_rad.save(output_ang_at)
         
    if suct == True:# se a flag de angulo de atrito for verdadeira, gera raster
         output_ang_at = os.path.join(output_gdb_par,'suct')
         ang_at_rad = Raster(sloperad)*0+suct_val
         ang_at_rad.save(output_ang_at)

    output_pesp_agua = os.path.join(output_gdb_par,'pesp_agua')
    pesp_agua = Raster(sloperad)*0+10
    pesp_agua.save(output_pesp_agua)

    output_pesp = os.path.join(output_gdb_par,'pesp')
    pesp = Raster(sloperad)*0+17
    pesp.save(output_pesp)

    output_htotal = os.path.join(output_gdb_par,'htotal')
    htotal = Raster(sloperad)*0+5
    htotal.save(output_htotal)

    output_hdrenagem = os.path.join(output_gdb_par,'hdrenagem')
    hdrenagem = Raster(sloperad)*0+2
    hdrenagem.save(output_hdrenagem)

    print 'Concluida a geracao de rasters de parametros'

###########################################################################################
################   CALCULA UM FATOR DE SEGURANCA  #########################################
    
    
    
def calculaFS(gdb_par):
    """
    Nele devem conter no minimo
    (1) o arquivo de declividades('slope'), (2) coesao('coes' (3) angulo de atrito em radianos('ang_at_rad') 
    (4) peso especifico do solo ('pesp')  (5) peso especifico da agua(pesp_agua'), 
    (6) altura de drenagem('hdrenagem') (7) altura total da camada de solo('htotal')
    """
       
    COES = os.path.join(gdb_par,'coes')
    if arcpy.Exists(COES) == False:
        print "Seu raster de coesao esta com o nome errado. Por favor, renomeie-o para 'coes' para que o programa\
        possa le-lo"
        
    suct = os.path.join(gdb_par,'suct')
    if arcpy.Exists(suct) == False:
        print "Seu raster de coesao esta com o nome errado. Por favor, renomeie-o para 'suct' para que o programa\
        possa le-lo"
    
    ang_at_rad = os.path.join(gdb_par,'ang_at_rad')
    if arcpy.Exists(ang_at_rad) == False:
        print "Seu raster de angulo de atrito esta com o nome errado. Por favor, renomeie-o para 'ang_at_rad' para que o programa\
        possa le-lo. Lembre-se que o raster angulo de atrito deve estar em radianos"
       
    htotal = os.path.join(gdb_par,'htotal')
    if arcpy.Exists(htotal) == False:
        print "Seu raster de angulo de htotal esta com o nome errado. Por favor, renomeie-o para 'htotal' para que o programa\
        possa le-lo"
        
    hdrenagem = os.path.join(gdb_par,'hdrenagem')
    if arcpy.Exists(hdrenagem) == False:
        print "Seu raster de angulo de hdrenagem esta com o nome errado. Por favor, renomeie-o para 'hdrenagem' para que o programa\
        possa le-lo"
        
    slope = os.path.join(gdb_par,'slope_rad')
    if arcpy.Exists(slope) == False:
        print "Seu raster de angulo de hdrenagem esta com o nome errado. Por favor, renomeie-o para 'hdrenagem' para que o programa\
        possa le-lo"
    
    pesp = os.path.join(gdb_par,'pesp')
    if arcpy.Exists(pesp) == False:
        print "Seu raster de angulo de pesp esta com o nome errado. Por favor, renomeie-o para 'pesp' para que o programa\
        possa le-lo."
        
    pesp_agua = os.path.join(gdb_par,'pesp_agua')
    if arcpy.Exists(pesp_agua) == False:
        print "Seu raster de angulo de pesp esta com o nome errado. Por favor, renomeie-o para 'pesp' para que o programa\
        possa le-lo."
        
    output_fs = os.path.join(gdb_par,'fs_single')
    fs = ((Raster(COES)+Raster(suct))/(Raster(htotal)*Raster(pesp) * Sin(Raster(slope)))) + (1-(Raster(hdrenagem)*Raster(pesp_agua)/(Raster(htotal)*Raster(pesp))))* (Cos(Raster(slope))*Tan(Raster(ang_at_rad))/Sin(Raster((slope))))
    
    fs.save(output_fs)
    print "O calculo do fator de seguranca para um conjunto foi finalizado. A saida esta em %s" % (output_fs)
    
   ###########################################################################################
########################   CODIGO DOS GERADORES DE NUMEROS ALEATORIOS    ##################    
def getrand_par(var_range_coes,var_range_ang_at, var_range_suct):
    
    a = np.random.randint(var_range_coes * -100  ,var_range_coes*100)/100.
    b = np.random.randint(var_range_ang_at * -100,var_range_ang_at*100)/100.
    c = np.random.randint(var_range_suct * -100,var_range_suct*100)/100.    
    return a,b,c
           
#########################################################################################  
################   SIMULADOR DE CENARIOS  ###############################################  
def simulaFS(gdb_par, gdb_scenarios, var_max_ang_atrito, var_max_coesao,var_max_suct,  nsim,logout):
#REDEFINE VARIAVEIS
    import os 
    var_suct = var_max_suct
    var_coes =  var_max_coesao
    var_ang_at = var_max_ang_atrito*3.141592/180
    arcpy.env.workspace = gdb_par
  
#PEGA OS RASTERS DE PARAMETROS DO gdb#
    print 'Lendo rasters da pasta...'
    COES = os.path.join(gdb_par,'coes')
    if arcpy.Exists(COES) == False:
        print "Seu raster de coesao esta com o nome errado. Por favor, renomeie-o para 'coes' para que o programa\
        possa le-lo"
    
    ang_at_rad = os.path.join(gdb_par,'ang_at_rad')
    if arcpy.Exists(ang_at_rad) == False:
        print "Seu raster de angulo de atrito esta com o nome errado. Por favor, renomeie-o para 'ang_at_rad' para que o programa\
        possa le-lo. Lembre-se que o raster angulo de atrito deve estar em radianos"
        
    suct = os.path.join(gdb_par,'suct')
    if arcpy.Exists(suct) == False:
        print "Seu raster de succao esta com o nome errado. Por favor, renomeie-o para 'suct' para que o programa\
        possa le-lo."
       
    htotal = os.path.join(gdb_par,'htotal')
    if arcpy.Exists(htotal) == False:
        print "Seu raster de angulo de htotal esta com o nome errado. Por favor, renomeie-o para 'htotal' para que o programa\
        possa le-lo"
        
    hdrenagem = os.path.join(gdb_par,'hdrenagem')
    if arcpy.Exists(hdrenagem) == False:
        print "Seu raster de angulo de hdrenagem esta com o nome errado. Por favor, renomeie-o para 'hdrenagem' para que o programa\
        possa le-lo"
        
    slope = os.path.join(gdb_par,'slope_rad')
    if arcpy.Exists(slope) == False:
        print "Seu raster de angulo de hdrenagem esta com o nome errado. Por favor, renomeie-o para 'hdrenagem' para que o programa\
        possa le-lo"
    
    pesp = os.path.join(gdb_par,'pesp')
    if arcpy.Exists(pesp) == False:
        print "Seu raster de angulo de pesp esta com o nome errado. Por favor, renomeie-o para 'pesp' para que o programa\
        possa le-lo."
        
    pesp_agua = os.path.join(gdb_par,'pesp_agua')
    if arcpy.Exists(pesp_agua) == False:
        print "Seu raster de angulo de pesp esta com o nome errado. Por favor, renomeie-o para 'pesp' para que o programa\
        possa le-lo."
    print 'A leitura dos rasters foi bem sucedida!'
#ITERADOR DA GERACAO DE CENARIOS###
    print 'Inicio da geracao de cenarios'
    logfolder = logout
    #print 'a pasta de saida do log e: %s. Caso queira mudar a pasta, altere os_cwd' % (fdr)
    logadress = os.path.join(logfolder, 'log.txt')
    if os.path.isfile(logadress) == True:
        os.remove(logadress)
    rand_list = [['coesao', 'angulo de atrito(rad)', 'succao']]
        
    k = 1 
    while k != nsim+1:
        scenario_number = 'scenario%s' %(k)
        adress = os.path.join(gdb_scenarios, scenario_number)
        a,b,c = getrand_par(var_range_coes=var_coes , var_range_ang_at = var_ang_at, var_range_suct = var_suct)
        fs_scenario = fs = ((Raster(COES)+a+Raster(suct)+c)/(Raster(htotal)*Raster(pesp) * Sin(Raster(slope)))) + (1-(Raster(hdrenagem)*Raster(pesp_agua)/(Raster(htotal)*Raster(pesp))))* (Cos(Raster(slope))*Tan(Raster(ang_at_rad)+b)/Sin(Raster((slope))))
        fs_scenario.save(adress)
        percent_done = (100*float(k)/(nsim))
        print '%.1f' % (percent_done) + r'% concluido'
        
        rand_list.append([a,b,c])
    
        k = k+1
           
    print 'Geracao de cenarios concluida, com saida na pasta %s' % (gdb_scenarios)
    print 'Gerando log...'
    openfile = open(logadress,'w')
    for item in rand_list:
        openfile.write("%s\n" % item)
    openfile.close()
#CALCULADOR DAS PROBABILIDADES POR MONTE CARLO PARA OS CENARIOS##
    print 'Inicio do calculo das probabilidades do cenario...'
    steps = nsim
    m = 1
    saida = os.path.join(gdb_par, 'raster_prob')
    while m != steps:
        if m ==1 :
            scenarios_step = 'scenario%s' % (m)
            arquivo = os.path.join(gdb_scenarios, scenarios_step)
            arcpy.CheckOutExtension("Spatial")
            out = Con(IsNull(arquivo), 0, arquivo)
            remap = arcpy.sa.RemapRange([[0,0.999,1], [1,9999,0]])
            outReclassify = arcpy.sa.Reclassify(arquivo, "VALUE", remap)
            outReclassify.save(arquivo)
    
            fs = Raster(arquivo)
            percent_done = 100*float(m)/(steps)
            print '%.1f' % (percent_done) + r'% concluido'
        else:
        
            scenarios_step = 'scenario%s' % (m)
            arquivo = os.path.join(gdb_scenarios, scenarios_step)
            arcpy.CheckOutExtension("Spatial")
            out = Con(IsNull(arquivo), 0, arquivo)
            remap = arcpy.sa.RemapRange([[0,0.999,1], [1,9999,0]])
            outReclassify = arcpy.sa.Reclassify(arquivo, "VALUE", remap)
            outReclassify.save(arquivo)
    
            fs = fs + Raster(arquivo)
            percent_done = 100*float(m)/(steps)
            print '%.1f' % (percent_done) + r'% concluido'           
        m = m+1
    divisor = float(steps)
    media = fs / divisor
    media.save(saida)
    print 'Calculo de probabilidades concluido.Programa terminado'
###########################################################################################

