using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System.Text;
using UnityEngine.UI;
using System.Collections;

using System.Threading;


public class clientRaspberry : MonoBehaviour
{
    public string IpAdress = "127.0.0.1";
    public int port = 8599;

    //Повороты головы
    private float RotationHeadX;
    private float RotationHeadY;

    //Управления с джостика
    private float JosticHorizontal;
    private float JosticVertical;
    private float JosticStop;

    //Глаза oculus
    private GameObject LeftEyeAnchor;
    private GameObject RightEyeAnchor;
    private GameObject CenterEyeAnchor;

    private GameObject left;
    private GameObject right;
    private GameObject Center;

    private Vector3 forwardRotate;

    public string message;
    public string sensor;
    private Socket socket;
    private GetRotation head;

    private void Start()
    {

        //для стерео зрения
        LeftEyeAnchor = GameObject.Find("LeftEyeAnchor");
        RightEyeAnchor = GameObject.Find("RightEyeAnchor");
        CenterEyeAnchor = GameObject.Find("CenterEyeAnchor");

        left = GameObject.Find("left");
        Center = GameObject.Find("Center");
        right = GameObject.Find("right");

        LeftEyeAnchor.transform.parent = left.transform;
        CenterEyeAnchor.transform.parent = Center.transform;
        RightEyeAnchor.transform.parent = right.transform;
        ///////////////////////////////////////////////////////////
        head = new GetRotation();
        head.glass = RightEyeAnchor;
        //
        ConnectServer();
        Thread mythread = new Thread(GetMessageServer);
        mythread.Start();


    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.S)) head.SetForwardRotate();
    }


    void FixedUpdate()
    {
        //Получаем данные с джостика
        //JosticHorizontal = Input.GetAxis("Submit") * 256f;
        //JosticVertical = Input.GetAxis("Vertical") * 256f;
        float A = Input.GetAxis("A");
        float B = Input.GetAxis("B");
        float Y = Input.GetAxis("Y");
        float X = Input.GetAxis("X");

        Debug.Log("A = " + A + " B = " + B + " Y = " + Y + " X = " + X);

        if (A == 1) JosticHorizontal = 1;
        else
        if (B == 1) JosticHorizontal = 2;
        else
        if (Y == 1) JosticHorizontal = 3;
        else
        if (X == 1) JosticHorizontal = 4;
        else
            JosticHorizontal = 0;


        Debug.Log("JosticHorizontal = " + JosticHorizontal);
        JosticStop = Input.GetAxis("Jump");

        //Получаем данные со шлема
        RotationHeadX = head.GetRotationX();
        RotationHeadY = head.GetRotationY();

        //Pos,x,y,Mot,h,v
        //
        message = "P," + RotationHeadX + "," + RotationHeadY + ",M," + JosticHorizontal + "," + JosticVertical + "," + JosticStop+ ",";
        SendMessageServer(message);

    }

    private void OnApplicationQuit()
    {
        DisconectServer();
    }

    //
   

    //Открыть соеденения
    private void ConnectServer()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.Connect(IpAdress, port);
        Debug.Log("Соеденения с сервером - Ok");
    }

    //Закрыть соеденения
    private void DisconectServer()
    {
        socket.Close();
        Debug.Log("Закрытия соеденения - Ok");
    }

    //отправить данные на Сервер
    private void SendMessageServer(string message)
    {
        //Debug.Log("send Message = " + message);
        byte[] buffer = Encoding.ASCII.GetBytes(message);
        socket.Send(buffer);
    }

    //Принять данные с сервера
    private void GetMessageServer()
    {
        while (true)
        {
            Debug.Log("Запрос на данные с сенсора");
            SendMessageServer("D");
            byte[] buffer = new byte[1024];
            socket.Receive(buffer);
            string volueSensor = Encoding.ASCII.GetString(buffer);
            sensor = volueSensor;
            Debug.Log("Данные пришли успешно");
            Thread.Sleep(5000);
        }
    }


    


   





}
