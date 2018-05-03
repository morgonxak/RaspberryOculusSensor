using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PanelSensot : MonoBehaviour {

    public GameObject client;

	
	// Update is called once per frame
	void Update () {
        string s = client.GetComponent<clientRaspberry>().sensor;
        string data = s.Substring(0, 2);
        
        
        string test = "Уровень Освещенности: " + data;
        string test2 = " люксов\nНорма освещенности: 310 люксов\nУровень СО2: 921 ppm\nНорма СО2: 800-1400 ppm\nТемпература воздуха: 22*С\nНорма температуры: 18-23*С\nОтносительная влажность воздуха: 32%\nНорма относительной влажности: <60%";
        string test3 = "Уровень Освещенности: " + data + " люксов\nНорма освещенности: 310 люксов\nУровень СО2: 921 ppm\nНорма СО2: 800-1400 ppm\nТемпература воздуха: 22*С\nНорма температуры: 18-23*С\nОтносительная влажность воздуха: 32%\nНорма относительной влажности: <60%";

        Debug.Log("lenS = " + test.Length);
        Debug.Log("lenS2 = " + test2.Length);
        Debug.Log("lenS3 = " + test3.Length);

        Debug.Log("test = " + data);
        Debug.Log("test2 = " + test2);
        Debug.Log("test3 = " + test3);
        this.GetComponent<Text>().text = test3;
    }
}
