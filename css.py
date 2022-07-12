def css(index=None):
    if index is None:
        return '<style>tbody th {display:none}.blank {display:none}</style>'
    return """
            <style>
            tbody th {display:none}.blank {display:none}
            tbody>:nth-child("""+str(index)+"""){
                background: #00ff00;
                font-size: 1.0em;
                font-weight: bold;
                }
            </style>
            """