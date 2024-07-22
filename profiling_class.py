import numpy as np
import math

class Profiling:
    """
    Class representing the perfilamento process.

    Attributes:
        profile (object): The profile object containing revenue, colab, and lawsuit attributes.
        standard_profile (float): The standard profile value.
        final_profile (float): The final profile value.
        partial_profile (float): The partial profile value.

    Methods:
        revenue: Calculates the revenue profile based on the profile's revenue attribute.
        colab: Calculates the colab profile based on the profile's colab attribute.
        lawsuit: Calculates the lawsuit profile based on the profile's lawsuit attribute.
        create_partial_profile: Creates the partial profile based on the profile's colab and lawsuit attributes.
        conflict_rule: Determines the conflict rule based on the partial profile and standard profile values.
        create_profile: Creates the final profile based on the revenue, colab, lawsuit, partial profile, and conflict rule.
    """

    def __init__(
            self, 
            profile, 
            weights = {'lawsuit': 1, 'colab': 1, 'revenue': 1}
        ):

        self.profile = profile
        self.standard_profile = np.nan
        self.final_profile = np.nan
        self.partial_profile = np.nan
        self.new_profile_rule = np.nan

        self.revenue_weight = weights['revenue']
        self.colab_weight = weights['colab']
        self.lawsuit_weight = weights['lawsuit']

        self.map_profile = {
            np.nan:'Sem perfil',
            1:'Mosca',
            2:'Pena',
            3:'Médio',
            4:'Pesado'
        }
        
    def revenue(self):
        """
        Calculates the revenue profile based on the profile's revenue attribute.

        Returns:
            int: The revenue profile value.
        """
        if (self.profile.revenue >= 0):
            if self.profile.revenue <= 60000:
                return 1
            elif self.profile.revenue <= 300000:
                return 2
            elif self.profile.revenue <= 1000000:
                return 3
            else:
                return 4
        return np.nan
    
    def colab(self):
        """
        Calculates the colab profile based on the profile's colab attribute.

        Returns:
            int: The colab profile value.
        """
        if (self.profile.colab >= 0):
            if self.profile.colab <= 3:
                return 1
            elif self.profile.colab <= 5:
                return 2
            elif self.profile.colab <= 10:
                return 3
            else:
                return 4
        return np.nan
    
    def lawsuit(self):
        """
        Calculates the lawsuit profile based on the profile's lawsuit attribute.

        Returns:
            int: The lawsuit profile value.
        """
        if (self.profile.lawsuit >= 0):
            if self.profile.lawsuit <= 100:
                return 1
            elif self.profile.lawsuit <= 300:
                return 2
            elif self.profile.lawsuit <= 1000:
                return 3
            else:
                return 4
        return np.nan
    
    def create_partial_profile(self):
        """
        Creates the partial profile based on the profile's colab and lawsuit attributes.

        Returns:
            int: The partial profile value.
        """
        if (self.profile.lawsuit >= 0) & (self.profile.colab >= 0):
            if self.profile.colab <=2:
                if self.profile.lawsuit <= 450:
                    return 1
                elif self.profile.lawsuit <= 800:
                    return 2
                elif self.profile.lawsuit <= 1300:
                    return 3
                else:
                    return 4
                
            elif self.profile.colab == 3:
                if self.profile.lawsuit <= 400:
                    return 1
                elif self.profile.lawsuit <= 700:
                    return 2
                elif self.profile.lawsuit <= 1250:
                    return 3
                else:
                    return 4
                
            elif self.profile.colab == 4:
                if self.profile.lawsuit <= 450:
                    return 1
                elif self.profile.lawsuit <= 800:
                    return 2
                elif self.profile.lawsuit <= 1300:
                    return 3
                else:
                    return 4
            
            elif self.profile.colab == 5:
                if self.profile.lawsuit <= 100:
                    return 1
                elif self.profile.lawsuit <= 450:
                    return 2
                elif self.profile.lawsuit <= 1150:
                    return 3
                else:
                    return 4
            
            elif self.profile.colab <= 7:
                if self.profile.lawsuit <= 100:
                    return 1
                elif self.profile.lawsuit <= 300:
                    return 2
                elif self.profile.lawsuit <= 100:
                    return 3
                else:
                    return 4
                
            else:
                if self.profile.lawsuit <= 100:
                    return 1
                elif self.profile.lawsuit <= 300:
                    return 2
                elif self.profile.lawsuit <= 1000:
                    return 3
                else:
                    return 4
                
        return np.nan

    def conflict_rule(self):
        """
        Determines the conflict rule based on the partial profile and standard profile values.

        Returns:
            int: The conflict rule value.
        """
        if self.partial_profile == 1:
            if self.standard_profile == 2:
                return 2
            elif self.standard_profile == 3:
                return 2
            elif self.standard_profile == 4:
                return 3

        elif self.partial_profile == 2:
            if self.standard_profile == 3:
                return 3
            elif self.standard_profile == 4:
                return 3

        elif self.partial_profile == 3:
            if self.standard_profile == 4:
                return 4
        
        return np.nan

    def new_rule(self, revenue, colab, lawsuit):
        """
        Calculates the new rule based on the revenue, colab, and lawsuit attributes.

        Returns:
            int: The new rule value.
        """
        if np.isnan(revenue):
            revenue = 0
            self.revenue_weight = 0
        if np.isnan(colab):
            colab = 0
            self.colab_weight = 0
        if np.isnan(lawsuit):
            lawsuit = 0
            self.lawsuit_weight = 0

        weighted_mean = (
            revenue*self.revenue_weight + colab*self.colab_weight + lawsuit*self.lawsuit_weight
            ) / (self.revenue_weight + self.colab_weight + self.lawsuit_weight)
        weighted_mean = int(math.ceil(weighted_mean))

        if weighted_mean > 6:
            weighted_mean = 5
            
        return weighted_mean
    
    def create_profile(self):
        """
        Creates the final profile based on the revenue, colab, lawsuit, partial profile, and conflict rule.

        Returns:
            list: A list containing the standard profile, partial profile, and final profile values.
        """
        try:
            revenue = self.revenue()
        except:
            revenue = np.nan
        
        try:
            colab = self.colab()
        except:
            colab = np.nan

        try:
            lawsuit = self.lawsuit()
        except:
            lawsuit = np.nan

        if (revenue is not np.nan) or (colab is not np.nan) or (lawsuit is not np.nan):

            self.standard_profile = revenue

            if (revenue == colab == lawsuit):
                self.final_profile = self.standard_profile

            else: 
                self.partial_profile = self.create_partial_profile()

                if (self.standard_profile is not np.nan) and (self.partial_profile is not np.nan):
                    if self.standard_profile <= self.partial_profile:
                        self.final_profile = self.partial_profile
                    else:
                        self.final_profile = self.conflict_rule()

                elif (self.standard_profile is np.nan) and (self.partial_profile is not np.nan):
                    self.final_profile = self.partial_profile
                
                else:
                    self.final_profile = np.nan
            try:
                self.new_profile_rule = self.new_rule(revenue, colab, lawsuit)
            except:
                pass

            profiles = [revenue, colab, lawsuit, self.partial_profile, self.final_profile, self.new_profile_rule]

            profiles = [self.map_profile[profile] for profile in profiles]

            profiles = {
                'Revenue profile':profiles[0],
                'Colab profile':profiles[1],
                'Lawsuit profile':profiles[2],
                'Parcial':profiles[3], 
                'Final':profiles[4], 
                'Nova':profiles[5]
            }
        
        else:
            profiles = {
                'Revenue profile':'Sem perfil',
                'Colab profile':'Sem perfil',
                'Lawsuit profile':'Sem perfil',
                'Parcial':'Sem perfil', 
                'Final':'Sem perfil', 
                'Nova':'Sem perfil'
            }

        return profiles