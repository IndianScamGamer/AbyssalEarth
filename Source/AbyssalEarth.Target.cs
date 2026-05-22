using UnrealBuildTool;
using System.Collections.Generic;

public class AbyssalEarthTarget : TargetRules
{
    public AbyssalEarthTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V6;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("AbyssalEarth");
    }
}
