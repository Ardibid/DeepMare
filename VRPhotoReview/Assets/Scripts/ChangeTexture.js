#pragma strict

 var matArray : Material[];
 private var index : int;
 
 function Update () {
     if (Input.GetButtonDown("Fire1")) {
         index++;
         index = index % matArray.Length;
         GetComponent.<Renderer>().sharedMaterial = matArray[index];
         Debug.Log("received event");
     }
 }

