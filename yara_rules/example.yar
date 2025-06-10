
rule ExampleRule
{
    strings:
        $a = "malicious"
    condition:
        $a
}
