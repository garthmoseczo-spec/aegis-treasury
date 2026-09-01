package com.aegistreasury;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.syntax.ArchRuleDefinition;
import org.junit.jupiter.api.Test;

public class ArchUnitTest {
    @Test
    public void layeredArchitectureExample() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.aegistreasury");
        ArchRuleDefinition.noClasses().that().resideInAPackage("..internal..")
            .should().beAccessedByAnyPackage("..external..");
    }
}
