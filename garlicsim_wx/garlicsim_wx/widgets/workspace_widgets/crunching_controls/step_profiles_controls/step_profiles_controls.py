# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.error_dialog import ErrorDialog

import garlicsim
import garlicsim_wx

from .step_profiles_list import StepProfilesList
from .step_profile_dialog import StepProfileDialog

from . import images as __images_package
images_package = __images_package.__name__

    
class StepProfilesControls(wx.Panel):
    '''tododoc'''
    
    def __init__(self, parent, frame, *args, **kwargs):
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundColour(wx_tools.get_background_color())

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_text = wx.StaticText(self, -1, 'Step profiles:')
        
        self.main_v_sizer.Add(self.title_text, 0, wx.ALL, 10)
        
        self.step_profiles_list = StepProfilesList(self, frame)
        
        self.main_v_sizer.Add(self.step_profiles_list, 1,
                              wx.EXPAND | wx.BOTTOM, 8)
        
        self.button_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.button_h_sizer, 0, wx.ALIGN_RIGHT)
        
        new_image = wx.BitmapFromImage(
            wx.ImageFromStream(
                pkg_resources.resource_stream(images_package,
                                              'new.png'),
                wx.BITMAP_TYPE_ANY
            )
        )
        self.new_button = wx.BitmapButton(self, -1, new_image)
        self.new_button.SetToolTipString('Create a new step profile.')
        
        self.button_h_sizer.Add(self.new_button, 0, wx.RIGHT, 8)
        
        delete_image = wx.BitmapFromImage(
            wx.ImageFromStream(
                pkg_resources.resource_stream(images_package,
                                              'trash.png'),
                wx.BITMAP_TYPE_ANY
            )
        )
        self.delete_button = wx.BitmapButton(self, -1, delete_image)
        self.delete_button.SetToolTipString(
            'Delete the selected step profile.'
        )
        self.delete_button.Disable()
        
        self.button_h_sizer.Add(self.delete_button, 0, wx.RIGHT, 8)
        
        self.SetSizer(self.main_v_sizer)
        
        
        self.Bind(wx.EVT_BUTTON, self.on_new_button, source=self.new_button)
        self.Bind(wx.EVT_BUTTON, self.on_delete_button, source=self.delete_button)

        
    def _recalculate(self):
        if self.step_profiles_list.get_selected_step_profile():
            self.delete_button.Enable()
        else: # self.step_profiles_list.get_selected_step_profile() is None
            self.delete_button.Disable()
            
    
    def show_step_profile_editing_dialog(self, step_profile=None):
        '''
        None for creating new step profile
        '''
        step_profile_dialog = StepProfileDialog(self, step_profile)
        
        try:
            if step_profile_dialog.ShowModal() == wx.ID_OK:
                new_step_profile = step_profile_dialog.step_profile
                new_hue = step_profile_dialog.hue
            else:
                new_step_profile = new_hue = None
                already_existing_step_profile = \
                    step_profile_dialog.step_profile
        finally:
            step_profile_dialog.Destroy()
            
        if new_step_profile:
            assert new_step_profile not in self.gui_project.step_profiles
            self.gui_project.step_profiles_to_hues[new_step_profile] = new_hue
            self.gui_project.step_profiles.add(new_step_profile)
            
        return new_step_profile or already_existing_step_profile

            

    def try_delete_step_profile(self, step_profile):
        # todo: in the future, make this dialog offer to delete the nodes with
        # the step profile.
        if step_profile is None:
            return
        tree_step_profiles = self.gui_project.project.tree.get_step_profiles()
        if step_profile in tree_step_profiles:
            error_dialog = ErrorDialog(
                self,
                "The step profile `%s` is currently used in the tree; It may "
                "not be deleted." % step_profile.__repr__(
                    short_form=True,
                    root=self.gui_project.simpack,
                    namespace=self.gui_project.namespace
                )
            )
            error_dialog.ShowModal()
            return
        else:
            self.gui_project.step_profiles.remove(step_profile)
            
            
    def on_new_button(self, event):
        self.show_step_profile_editing_dialog(step_profile=None)
    
    
    def on_delete_button(self, event):
        self.try_delete_step_profile(
            self.step_profiles_list.get_selected_step_profile()
        )