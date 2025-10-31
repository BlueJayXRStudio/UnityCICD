using UnityEditor;
using UnityEditor.Build.Reporting;
using System;
using System.IO;
using UnityEditor.Build;

/// <summary>
/// Must be stored under Assets/Editor
/// </summary>
public static class MacOSServerBuildCommand
{
    // Example: Apple Silicon (ARM64) dedicated server build
    public static void BuildMacServer()
    {
        // Choose output path
        string[] args = Environment.GetCommandLineArgs();
        string buildPath = GetArgValue(args, "buildPath") ?? "Builds/MacServer_arm64/MyGameServer";

        // Define scenes to include
        string[] scenes = new[]
        {
            "Assets/Scenes/SampleScene.unity",
        };

        // Set build player options
        var buildPlayerOptions = new BuildPlayerOptions
        {
            scenes = scenes,
            locationPathName = buildPath,
            target = BuildTarget.StandaloneOSX,
            subtarget = (int)StandaloneBuildSubtarget.Server
        };

        bool switched = EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.Standalone, BuildTarget.StandaloneOSX);
        if (!switched)
        {
            Console.WriteLine("Failed to switch to macOS build target. Check if macOS build support is installed.");
            return;
        }

        // Set scripting backend to IL2CPP
        PlayerSettings.SetScriptingBackend(NamedBuildTarget.Server, ScriptingImplementation.IL2CPP);
        // Set architecture to ARM64
        PlayerSettings.SetArchitecture(BuildTargetGroup.Standalone, 1); // 0 = x86_64 (Intel), 1 = ARM64 (Apple Silicon)
        
        // Perform the build
        var report = BuildPipeline.BuildPlayer(buildPlayerOptions);

        if (report.summary.result == UnityEditor.Build.Reporting.BuildResult.Succeeded)
            Console.WriteLine("Build completed successfully: " + buildPath);
        else
            Console.WriteLine("Build failed: " + report.summary.result);
    }

    // Helper to parse CLI args like buildPath=...
    private static string GetArgValue(string[] args, string name)
    {
        foreach (var arg in args)
        {
            if (arg.StartsWith(name + "=", StringComparison.OrdinalIgnoreCase))
                return arg.Substring(name.Length + 1);
        }
        return null;
    }
}