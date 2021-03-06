# -*- coding: UTF-8 -*-

""" 
``MODULE_NAME``
-----------------------------------------------------------------


:Authors: AUTHOR
:Affiliation: AFFILITATION
:Organization: ORGANIZATION

SHORT DESCRIPTION OF PROGRAM THIS MODULE IS BUILT TO EXECUTE


Requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* SHORT DESCRTIPTION OF FILE TYPE EXPECTED TO EXIST

    * ``sample_data[<sample>]["FILE_TYPE"]``

* ...

Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* SHORT DESCRTIPTION OF FILE TYPE PRODCED

    * ``self.sample_data[<sample>]["FILE_TYPE"])``
    * ...

* ...
     
    
Parameters that can be set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: 
    :header: "Parameter", "Values", "Comments"
    :widths: 15, 10, 10

    "PARAMETER", "POSSIBLE VALUES", "SHORT DESCRIPTION"

Lines for parameter file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    INSTANCE_NAME:
        module: MODULE_NAME
        base: BASE_NAME
        script_path: /PATH/TO/PROGRAM
        redirects:
            A FEW EXAMPLES OF REDIRECTED PARAMETERS


References
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NAMES, YEAR. **TITLE**. *JOURNAL*, EDITION, pp.PAGES.

"""

import os
import sys
from neatseq_flow.PLC_step import Step,AssertionExcept


__author__ = "Author"

class Step_MODULENAME(Step):

    # A list of parameters the user should NOT redirect:
    auto_redirs = "-i --in -o --out".split(" ")
    
    def step_specific_init(self):
        self.shell = "bash"      # Can be set to "csh" by inheriting instances.

        # This module can use both scopes.
        # If 'scope' is defined, check it
        if "scope" in self.params:
            if self.params["scope"] not in ["project","sample"]:
                raise AssertionExcept("'scope' must be either 'sample' or 'project'")
        # If 'scope' is not defined, use 'sample' as default
        else:
            self.params["scope"] = "sample"

        # Various assertions
        if CONDITION:
            raise AssertionExcept("ERROR MESSAGE\n")

    def step_sample_initiation(self):
        """ A place to do initiation stages following setting of sample_data
        """

        # Setting sample list according to scope
        if self.params["scope"] == "project":
            self.sample_list = ["project_data"]
        else:  # self.params["scope"] == "sample" !
            self.sample_list = self.sample_data["samples"]

        # Testing a condition on each sample
        # Useful for making sure all samples include the input files required by the module.
        for sample in self.sample_data["samples"]:      # Getting list of samples out of samples_hash
            if (CONDITION ON sample_data):
                raise AssertionExcept("ERROR MESSAGE\n")

    def create_spec_wrapping_up_script(self):
        """ Define self.script to add a script to be executed after all other scripts have terminated
        """
        pass
        
    def create_spec_preliminary_script(self):
        """ Define self.script to add a script to be executed BEFORE ALL other step scripts 
        """
        pass

    def build_scripts(self):
        """ This is the actual script building function
            Most, if not all, editing should be done here 
        """
        
        # Loop over list of samples out of samples_hash and create script for each sample
        # Note! self.sample_list is either a list of samples (scope=sample) or ["project_data"] (scope=project)
        for sample in self.sample_list:

            # Make a dir for the current sample:
            sample_dir = self.make_folder_for_sample(sample)

            # Name of specific script:
            self.spec_script_name = self.set_spec_script_name(sample)
            self.script = ""
            
            # This line should be left before every new script. It sees to local issues.
            # Use the dir it returns as the base_dir for this step.
            use_dir = self.local_start(sample_dir)

            # Define location and prefix for output files:
            # You can replace _MODULE_SUFFIX with anything you like.
            output_prefix = use_dir + sample + "_MODULE_SUFFIX"
            
            # Get constant part of script:
            # Adds lines for environmental variables, script path and redirected parameters
            self.script += self.get_script_const()
            # Specifically add input and output files:
            # This changes per module. The input files MUST BE taken from the sample_data dictionary!
            self.script += "%s \\\n\t" % self.sample_data[sample]["INPUT_FILE_TYPE"]
            self.script += "%s \n\n" % output_prefix

            # Put the output file/s in the sample_data dictionary
            # If output file is standard format, put in suitable slot. 
            # If not, you can invent a slot for it, in a sensible way.
            self.sample_data[sample]["OUTPUT_FILE_TYPE1"] = sample_dir + sample + "_MODULE_SUFFIX"
            self.sample_data[sample]["OUTPUT_FILE_TYPE2"] = ...
            # Mark file for md5 stamping in log files:
            # Repeat for each file created by the module that you wish to stamp
            self.stamp_file(self.sample_data[sample]["OUTPUT_FILE_TYPE"])
           
 
            # Move all files from temporary local dir to permanent base_dir
            self.local_finish(use_dir,sample_dir)       
        
            # Required line. Leave as is.
            self.create_low_level_script()
                        
    def make_sample_file_index(self):
        """ Make file containing samples and target file names.
            see blast module for implementation.
        """
        pass
