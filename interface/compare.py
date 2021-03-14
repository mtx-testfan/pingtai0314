class Compare:
    def eqls(self,actual,expected):
        '''
        相等
        actual 实际结果
        expected  预期结果
        :return:
        '''
        return actual  == expected

    def gt(self,actual,expected):
        '''
        相等
        actual 实际结果
        expected  预期结果
        :return:
        '''
        return actual  > expected

    def lt(self,actual,expected):
        '''
        相等
        actual 实际结果
        expected  预期结果
        :return:
        '''
        return actual  < expected
    def gte(self,actual,expected):
        '''
        相等
        actual 实际结果
        expected  预期结果
        :return:
        '''
        return actual  >= expected

    def lte(self,actual,expected):
        '''
        相等
        actual 实际结果
        expected  预期结果
        :return:
        '''
        return actual  <= expected