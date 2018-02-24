// Adapted from: https://www.youtube.com/watch?v=U-L0COB3lys

using System.Collections;
using UnityEngine;

public class control : MonoBehaviour {
    // make an instance of the class valve.VR.EVRButtonId to act as the trigger
    private Valve.VR.EVRButtonId triggerButton = Valve.VR.EVRButtonId.k_EButton_SteamVR_Trigger;
    // declare device and trackobject to address the controller
    private SteamVR_TrackedObject trackedObject;
    private SteamVR_Controller.Device device;

	// Initializing the functions
	void Start () {
        trackedObject = GetComponent<SteamVR_TrackedObject>();
	}
	
	// Updates the scene in every frame
	void update ()
    {
        device = SteamVR_Controller.Input((int)trackedObject.index);
        if (device.GetPress(triggerButton))
        {
            device.TriggerHapticPulse(500);
        }
        if (device.GetPressDown(triggerButton))
        {
            device.TriggerHapticPulse(1000);
        }
		
	}
}
