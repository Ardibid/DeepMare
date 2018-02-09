// adapted from: https://github.com/UoA-eResearch/PhotosphereViewer

// for basic unity functionality
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


// for lookng up in the folder
using System;
using System.IO;
using System.Reflection;

public class thumbnail_01 : MonoBehaviour {
    // making a list of all avilable background scenes
    public Material[] scenes;

    List <Texture2D> textures = new List<Texture2D>();
    // the final renering material for the scene
    List<Material> materials = new List<Material>();
    List<string> textureNames = new List<string>();
    List<Material> updatedMaterials = new List<Material>();
    public Shader shader;
    public Color color;

    // rendering method for the spehre 
    private Renderer ren;
    // index to navigate through materials 
    private int index = 3;

	// Use this for initialization
	void Start () {
        ren = GetComponent<Renderer>();
	}
	
	// Update is called once per frame
	void Update ()
    {
        // get the index of the controllers
        var left = SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Leftmost);
        var right = SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Rightmost);
        // Chekc if the left cotroller is available and the trigger is fully pressed 
        if (left != -1 && SteamVR_Controller.Input(left).GetPressDown(SteamVR_Controller.ButtonMask.Trigger))
        {
            // add the event to the log, activates the haptic feedback on the cotroller
            Debug.Log("Left is pressed!");
            SteamVR_Controller.Input(left).TriggerHapticPulse(1000);
            // increases the index by one
            index++;
        }
        else if (right != -1 && SteamVR_Controller.Input(right).GetPressDown(SteamVR_Controller.ButtonMask.Trigger))
        {
            // add the event to the log, activates the haptic feedback on the cotroller
            Debug.Log("Right is pressed!");
            SteamVR_Controller.Input(right).TriggerHapticPulse(1000);
            // decreases the index by one
            index--;
        }

        // updates the material library by scanning the material folder
        if (left != -1 && SteamVR_Controller.Input(left).GetPressDown(SteamVR_Controller.ButtonMask.ApplicationMenu))
        {
            Debug.Log("Updating the image database!");
            // wipes out the currently available textures
            textures.Clear();
            // setting the constant values for the materials
            Material tempMaterial = new Material(Shader.Find("Flip Normals"));
            Texture2D tex = null;
            // checks for all the available jpg files in the material folder
            var path = Directory.GetCurrentDirectory()+ "\\Assets\\Material";
            string[] names = Directory.GetFiles(path);
            foreach (string name in names)
            {
                // check files extensions, collect all .JPGs
                string extension = Path.GetExtension(name);
                if (extension == ".jpg" )
                {
                    // collects the file data, all pixels!
                    var fileData = File.ReadAllBytes(name);
                    // saves the data as a texture file
                    tex = new Texture2D(2, 2);
                    tex.LoadImage(fileData);
                    tempMaterial.mainTexture = tex;
                    // add textures to the library
                    textures.Add(tex);

                }   
            }
            Debug.Log(textures.Count);
        }
            if (ren != null)
        {
            var tmpLen = scenes.Length;
            if (updatedMaterials.Count == 0)
                {
                 ren.material = scenes[Mathf.Abs(index) % tmpLen];
                }
            if (textures.Count != 0)
             {
                tmpLen = textures.Count;
                // apply material 
                var modifiedIndex = Mathf.Abs(index) % tmpLen;
                ren.material.mainTexture= textures[Mathf.Abs(index) % tmpLen];
                 }
                 
        }
    }
}
