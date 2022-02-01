#coding: utf-8

#Dhyego Lancaster

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from reportlab.pdfgen import canvas
import time

#print('Online')
#declarabdo variavel global para func editar_salvar
numero_id = 0

def funcao_principal():
    #nome
    linha1 = cadastroabordados.lineEdit.text()
    #nome da mae
    linha2 = cadastroabordados.lineEdit_2.text()
    #nascimento
    linha3 = cadastroabordados.dateEdit.text()
    #endereco
    linha4 = cadastroabordados.lineEdit_3.text()
    #artigos
    linha5 = cadastroabordados.lineEdit_4.text()
    #observacao
    linha6 = cadastroabordados.lineEdit_5.text()
    #sexo
    linha7 = cadastroabordados.comboBox.currentText()

#inserindo no BD
    # conectando BD...
    conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
    # definindo um cursor
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS abordado(id INTEGER not null primary KEY autoincrement, nome TEXT, mae TEXT, dn TEXT, endereco TEXT, artigos TEXT, obs TEXT, sexo TEXT)")
    cursor.execute("""
    INSERT INTO abordado(nome, mae, dn, endereco, artigos, obs,sexo) 
    VALUES(?,?,?,?,?,?,?)
    """, (linha1, linha2, linha3, linha4, linha5, linha6, linha7))
    conn.commit()
    QMessageBox.about(cadastroabordados, "Atenção", "Feito com Sucesso!")
    #print("Enviado com SUCESSO...")

    #limpas os campos
    cadastroabordados.lineEdit.setText("")
    cadastroabordados.lineEdit_2.setText("")
    cadastroabordados.lineEdit_3.setText("")
    cadastroabordados.lineEdit_4.setText("")
    cadastroabordados.lineEdit_5.setText("")

def gerar_pdf():
    # listando no BD
    conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
    # definindo um cursor
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM abordado;")
    linha = cursor.fetchall()
    y=0
    pdf=canvas.Canvas("lista_de_abordados.pdf")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(200,800, "Listagem:")
    pdf.setFont("Times-Bold", 8)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(40,750, "NOME")
    pdf.drawString(140,750, "Nome da Mãe")
    pdf.drawString(230, 750, "Data Nascimento")
    pdf.drawString(300, 750, "Endereço")
    pdf.drawString(450, 750, "Artigos")
    pdf.drawString(510, 750, "OBS")
    pdf.drawString(640, 750, "Sexo")

    for i in range(0, len(linha)):
        y = y + 20
        pdf.drawString(10, 750 - y, str(linha[i][0]))
        pdf.drawString(40, 750 - y, str(linha[i][1]))
        pdf.drawString(140, 750 - y, str(linha[i][2]))
        pdf.drawString(230, 750 - y, str(linha[i][3]))
        pdf.drawString(300, 750 - y, str(linha[i][4]))
        pdf.drawString(450, 750 - y, str(linha[i][5]))
        pdf.drawString(510, 750 - y, str(linha[i][6]))
        pdf.drawString(640, 750 - y, str(linha[i][7]))
    pdf.save()
    QMessageBox.about(segundatela, "Atenção", "Feito com Sucesso!")
    #print("PDF foi gerado com SUCESSO!")
    conn.close()


def chama_segundatela():
    segundatela.show()
#listando no BD
    conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
    # definindo um cursor
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM abordado;")
    linha = cursor.fetchall()
    #dimensiona o tamanho da coluna
    segundatela.tableWidget.setRowCount(len(linha))
    segundatela.tableWidget.setColumnCount(8)
    segundatela.tableWidget.setColumnWidth(0, 30)
    segundatela.tableWidget.setColumnWidth(1, 140)
    segundatela.tableWidget.setColumnWidth(2, 130)
    segundatela.tableWidget.setColumnWidth(3, 70)
    segundatela.tableWidget.setColumnWidth(4, 160)
    segundatela.tableWidget.setColumnWidth(5, 50)
    segundatela.tableWidget.setColumnWidth(6, 100)

    for i in range(0, len(linha)):
        for j in range(0, 8):
            segundatela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(linha[i][j])))

def excluir_dado():
   excluir = segundatela.tableWidget.currentRow()
   segundatela.tableWidget.removeRow(excluir)
   # conectando BD...
   conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
   # definindo um cursor
   cursor = conn.cursor()
   cursor = conn.cursor()
   cursor.execute("SELECT id FROM abordado;")
   linha = cursor.fetchall()
   valor_id = linha[excluir][0]
   cursor.execute("DELETE FROM abordado WHERE id="+ str(valor_id))
   conn.commit()
   QMessageBox.about(segundatela, "Atenção", "Feito com Sucesso!")

def editar_dado():
    global numero_id
    #editartela.show()
    editar = segundatela.tableWidget.currentRow()

    # conectando BD...
    conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
    # definindo um cursor
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM abordado;")
    linha = cursor.fetchall()
    valor_id = linha[editar][0]
    cursor.execute("SELECT * FROM abordado WHERE id=" + str(valor_id))
    editou = cursor.fetchall()
    #print(editou[0][0])
    #print(editou[0][4])

    numero_id = valor_id

    editartela.show()
    # nome
    editartela.lineEdit.setText(str(editou[0][1]))
    # nome da mae
    editartela.lineEdit_2.setText(str(editou[0][2]))
    # nascimento
    #editartela.dateEdit.setText(str(editou[0][3]))
    # endereco
    editartela.lineEdit_3.setText(str(editou[0][4]))
    # artigos
    editartela.lineEdit_4.setText(str(editou[0][5]))
    # observacao
    editartela.lineEdit_5.setText(str(editou[0][6]))
    # sexo
    #editartela.comboBox.settext(str(editou[0][7]))
    #conn.commit()
def editar_salvar():
    #pega o numero que cliente selecionou
    global numero_id
    # nome
    linha1a = editartela.lineEdit.text()
    # nome da mae
    linha2a = editartela.lineEdit_2.text()
    # nascimento
    linha3a = editartela.dateEdit.text()
    # endereco
    linha4a = editartela.lineEdit_3.text()
    # artigos
    linha5a = editartela.lineEdit_4.text()
    # observacao
    linha6a = editartela.lineEdit_5.text()
    # sexo
    linha7a = editartela.comboBox.currentText()
#atualizando no BD
    # conectando BD...
    conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
    # definindo um cursor
    cursor = conn.cursor()
    cursor.execute("UPDATE abordado SET nome = ?, mae = ?, dn = ?, endereco = ?, artigos = ?, obs = ?,sexo = ? WHERE id= ?", (linha1a, linha2a, linha3a, linha4a, linha5a, linha6a, linha7a, str(numero_id)))
    conn.commit()
    QMessageBox.about(editartela, "Atenção", "Feito com Sucesso!")
    #print("Atualizado...")
    editartela.close()
    segundatela.close()
    chama_segundatela()

    #print("Atualizado...")


def limpa_tela():
    # limpas os campos
    cadastroabordados.lineEdit.setText("")
    cadastroabordados.lineEdit_2.setText("")
    cadastroabordados.lineEdit_3.setText("")
    cadastroabordados.lineEdit_4.setText("")
    cadastroabordados.lineEdit_5.setText("")
def logar():
    loguintela.label_5.setText("")
    nome_usuario = loguintela.lineEdit.text()
    senha = loguintela.lineEdit_2.text()

    # conectando BD...
    conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
    # definindo um cursor
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM loguin WHERE usuario='{}'".format(nome_usuario))
    senha_bd = cursor.fetchall()
   # if nome_usuario == "":
     #   loguintela.label_5.setText("Loguin ou Senha, VAZIOS!")
    if senha == senha_bd[0][0]:
        QMessageBox.about(loguintela,"Atenção","Login Feito com Sucesso!")
        loguin2.show()
        loguintela.close()
    else :
        loguintela.label_5.setText("Loguin ou Senha, INCORRETOS!")


def deslogar():
    loguin2.close()
    loguintela.show()
    loguintela.lineEdit.setText("")
    loguintela.lineEdit_2.setText("")
def ir_cadastro():
    #vai pro cadastro abordado
    loguintela.close()
    loguin2.close()
    cadastroabordados.show()

def ir_cadastrologuin():
    #vai pro cadastro de usuario
    loguincadastro.show()
def cadastrologuin():
    #enviar e cadastro o novo usuario
    usuario = loguincadastro.lineEdit.text()
    senha = loguincadastro.lineEdit_2.text()
    repitasenha = loguincadastro.lineEdit_3.text()

    if (senha == repitasenha):
        try:
            # conectando BD...
            conn = sqlite3.connect('C:/sqlite2021/aula/banco.db')
            # definindo um cursor
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS loguin(usuario text, senha text)")
            cursor.execute("INSERT INTO loguin(usuario, senha) VALUES(?,?)", (usuario, senha))

            conn.commit()
            conn.close()
            QMessageBox.about(loguincadastro, "Atenção", "Feito com Sucesso!")
            time.sleep(1)
            loguincadastro.close()

            #loguintela.show()
        except sqlite3.Error as erro:
            print("Erro ao inserir dados: ",erro)
    else:
        loguincadastro.label_3.setText("As senhas estão diferentes")




app = QtWidgets.QApplication([])
#as telas
cadastroabordados=uic.loadUi("cadastroabordados.ui")
segundatela=uic.loadUi("listaabordados.ui")
editartela=uic.loadUi("editarabordados.ui")
loguintela=uic.loadUi("loguin.ui")
loguin2=uic.loadUi("loguin2.ui")
loguincadastro=uic.loadUi("loguincadastro.ui")

#botoes que chamam as funçoes
cadastroabordados.pushButton.clicked.connect(funcao_principal)
cadastroabordados.pushButton_2.clicked.connect(chama_segundatela)
cadastroabordados.pushButton_3.clicked.connect(limpa_tela)
segundatela.pushButton.clicked.connect(gerar_pdf)
segundatela.pushButton_2.clicked.connect(excluir_dado)
segundatela.pushButton_3.clicked.connect(editar_dado)
editartela.pushButton.clicked.connect(editar_salvar)
loguintela.pushButton_2.clicked.connect(logar)
loguintela.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
loguin2.pushButton_2.clicked.connect(deslogar)
loguin2.pushButton_4.clicked.connect(chama_segundatela)
loguin2.pushButton_5.clicked.connect(ir_cadastro)
loguintela.pushButton.clicked.connect(ir_cadastrologuin)
loguincadastro.pushButton_2.clicked.connect(cadastrologuin)

#finaliza appp
loguintela.show()
app.exec()
