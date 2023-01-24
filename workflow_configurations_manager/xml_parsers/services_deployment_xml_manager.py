# ------------------------------------------------------------------------------
#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor
#  license agreements; and to You under the Apache License, Version 2.0. "
#
# Forschungszentrum Jülich
#  Institute: Institute for Advanced Simulation (IAS)
#    Section: Jülich Supercomputing Centre (JSC)
#   Division: High Performance Computing in Neuroscience
# Laboratory: Simulation Laboratory Neuroscience
#       Team: Multi-scale Simulation and Design
#
# ------------------------------------------------------------------------------

# Co-Simulator's import
from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers import enums
from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers import xml_tags
# from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers import constants
from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers.xml_manager import XmlManager


class ServicesDeploymentXmlManager(XmlManager):
    """
        XML Manager for the Co-Sim Services Deployment XML file
        TO-BE-DONE: Even thought the deployment of Co-Simulation services
            (e.g. orchestrator, launcher) is oriented to be used
             on HPC systems, it is german to consider similar approach
             on local systems where multiple cores could be used.
    """

    def __init__(self, log_settings, configurations_manager, xml_filename, name):
        super().__init__(log_settings, configurations_manager, xml_filename, name)

        self.__services_deployment_dict = None

    def initialize_xml_elements(self):
        # TO BE DONE: there should be a global XML file where tags are defined
        self._component_xml_tag = xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_ROOT_TAG

    def _build_variables_dict_from_xml_main_dicts(self):
        """
            Avoiding the presence of the <variable></variables> section on the XML file

        :return:

            XML_OK: Mimicking <variables> section parsing process was successful.
        """

        return enums.XmlManagerReturnCodes.XML_OK

    def _build_parameters_dict_from_xml_main_dicts(self):
        """
            Avoiding the presence of the <parameters> ... </parameters> section on the XML file

        :return:

            XML_OK: Mimicking <parameters> ... </parameters> section parsing process was successful.
        """

        return enums.XmlManagerReturnCodes.XML_OK

    def build_particular_sections_dicts(self):
        return enums.XmlManagerReturnCodes.XML_OK

    def build_particular_sections_dicts(self):
        """

        :return:
            XML_ERROR
            XML_OK
        """
        self.__services_deployment_dict = {}

        #
        # STEP 1 - srun command line options

        try:
            srun_options_raw_string = \
                self._main_xml_sections_dicts_dict[xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SRUN_OPTIONS]
        except KeyError:
            self._logger.error('{} has no <{}>...</{}> section'.format(self._xml_filename,
                                                                       xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SRUN_OPTIONS,
                                                                       xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SRUN_OPTIONS))
            return enums.XmlManagerReturnCodes.XML_TAG_ERROR

        tmp_srun_options = srun_options_raw_string.strip()  # removing new line chars
        # the string from the XML file into a python list, e.g.
        # ['srun', '--exact', '--label', '--nodes=1', '--ntasks=1', '--cpus-per-task=1',
        # '--cpu-bind=none', '--gres=gpus:0']
        # TO BE DONE: Additional validations related to, e.g. "srun" presence in the string
        self.__services_deployment_dict[
            xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SRUN_OPTIONS] = tmp_srun_options.split(" ")  # python list

        #
        # STEP 2 - Co-Sim Services HPC Nodes Arrangement
        try:
            self.__services_deployment_dict[xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SETTINGS] = \
                self._main_xml_sections_dicts_dict[xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SETTINGS]
        except KeyError:
            self._logger.error('{} has no <{}>...</{}> section'.format(self._xml_filename,
                                                                       xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SETTINGS,
                                                                       xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SETTINGS))
        self.__services_deployment_dict[xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SETTINGS] = \
            self._main_xml_sections_dicts_dict[xml_tags.CO_SIM_XML_CO_SIM_SERVICES_DEPLOYMENT_SETTINGS]

        return enums.XmlManagerReturnCodes.XML_OK

    def _TMP_build_particular_sections_dicts(self):
        """
            - Implements the abstract method which is called at the end of the
            Co-Simulation XML file dissection process.
            - Converts into INTEGER those members of the dictionary whose value is expected to be numerical.

        :return:
            XML_VALUE_ERROR -> When some string cannot be converted into INTEGER
            XML_OK:         -> All the values were converted into INTEGER as expected.
        """

        #
        # processing the communication dictionary with the following format:
        # {
        #   'ORCHESTRATOR': {'MIN': '59100', 'MAX': '59120', 'MAX_TRIES': '20'},
        #   'COMMAND_CONTROL': {'MIN': '59121', 'MAX': '59150', 'MAX_TRIES': '30'},
        #   'APPLICATION_COMPANION': {'MIN': '59150', 'MAX': '59200', 'MAX_TRIES': '50'}
        # }
        # 2022-09-21: So far all the components will be treated similarly,
        #             meaning MAX MIN MAX_TRIES being INTEGER
        #
        for key, value in self._main_xml_sections_dicts_dict.items():
            # key -> represents a CO-SIM Component, e.g. ORCHESTRATOR

            try:
                value['MIN'] = int(value['MIN'])
                value['MAX'] = int(value['MAX'])
                value['MAX_TRIES'] = int(value['MAX_TRIES'])
            except ValueError:
                self._logger.error(ValueError)
                return enums.XmlManagerReturnCodes.XML_VALUE_ERROR

        return enums.XmlManagerReturnCodes.XML_OK

    def get_services_deployment_dict(self):
        """
            Returns the list containing the srun options used to start the Co-Sim Services

            :return:
                A list containing srun command and its options
        """

        # getting the dictionary from the parent class
        return self.__services_deployment_dict
