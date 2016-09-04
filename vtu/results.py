from vtu.processors.regular import RegularResultProcessor


def get_results(usn, results_type='regular', output_format='dict'):
    """
    The entry point to get results for a given usn.
    :param usn: A unique id of a student.
    :param type: Specify the type of results. Possible values are regular, revaluation, backlog.
    """

    if results_type == 'regular':
        results = RegularResultProcessor(usn=usn, output_format=output_format).process()
    else:
        # TODO
        raise NotImplementedError('The results_type %s has not been implemented yet!.' % results_type)

    return results
def get_cbcs_results(usn,sem,results_type='regular'):
    """
    Get the choiced based credit system results
    usage:
        result=get_cbcs_results('4pa15cs045',2,regular(optinal))
    output
    {   'name': 'KHADEEJA HANNATH N B',

        'marksheet':[
            ['ENGINEERING MATHS-II', '15MAT21', '4', '4', 'E', '4', '16', ''], 
            ['ENGINEERING CHEMISTRY', '15CHE22', '4', '4', 'E', '4', '16', ''], 
            ['PROGRAMMING IN C & DATA STRUCTURES', '15PCD23', '4', '4', 'E', '4', '16', ''],
            ['COMPUTER AIDED ENGINEERING DRAWING', '15CED24', '4', '4', 'D', '5', '20', ''], 
            ['BASIC ELECTRONICS', '15ELN25', '4', '4', 'E', '4', '16', ''],
            ['COMPUTER PROGRAMMING LAB.', '15CPL26', '2', '2', 'S+', '10', '20', ''],
            ['ENGINEERING CHEMISTRY LAB.', '15CHEL27', '2', '2', 'B', '7', '14', ''], 
            ['ENVIRONMENTAL STUDIES', '15CIV28', '0', '0', 'P', '0', '0', '']
        ]
    }
    """
    if int(usn[3:5])>=15 and results_type=='regular':
        results=RegularResultProcessor.fetch_cbcs_results(usn,sem)
        return results
    else:
        return None