using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{

    private Rigidbody2D rb2D;

    void Start()
    {
        rb2D = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            rb2D.velocity = new Vector3(Random.Range(-10, 10), Random.Range(-10, 10), 0).normalized * 2;
        }
        if (Input.GetKeyDown(KeyCode.E)) {
            rb2D.velocity = new Vector3(Random.Range(-10, 10), 0, 0).normalized * 2;
        }
        if (Input.GetKeyDown(KeyCode.D)) {
            rb2D.velocity = new Vector3(0, Random.Range(-10, 10), 0).normalized * 2;
        }
    }
}