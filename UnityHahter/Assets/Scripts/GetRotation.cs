using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetRotation : MonoBehaviour {
    public GameObject glass;
    private Vector3 forwardRotate;

	void Start () {
		glass = GameObject.Find("RightEyeAnchor");
    }
	
	void Update () {
        if (Input.GetKeyDown(KeyCode.S)) SetForwardRotate();

        Debug.Log(GetRotationY());
        Debug.Log(GetRotationX());

        if (Input.GetKey("escape"))
            Application.Quit();

    }


    public void SetForwardRotate ()
    {
        forwardRotate = glass.transform.rotation.eulerAngles;
    }

    public float GetRotationY ()
    {
        float y = forwardRotate.y - glass.transform.rotation.eulerAngles.y;
        if (y > 180) y = (y - 180) * -1;
        if (y < -180) y = (y + 180) * -1;

        y += 90;

        return y;
    }

    public float GetRotationX()
    {
        float y = glass.transform.rotation.eulerAngles.x;
        if (y < 180) y = y + 90;
        if (y > 270) y = y - 270;

        return y;
    }
}
